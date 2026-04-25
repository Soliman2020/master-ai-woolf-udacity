from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional
import os
import asyncio

# RAGAS imports - handle different module structures across versions
RAGAS_AVAILABLE = False
_import_errors = []

try:
    from ragas import SingleTurnSample
    from ragas import evaluate
    # Try newer metric structure first
    try:
        from ragas.metrics import ResponseRelevancy, Faithfulness
        _new_metrics = True
    except ImportError:
        _new_metrics = False

    # Try non-LLM metrics from collections
    try:
        from ragas.metrics._metrics import BleuScore, RougeScore
        from ragas.metrics._context_precision import NonLLMContextPrecisionWithReference
        _collection_metrics = True
    except ImportError:
        try:
            from ragas.metrics import BleuScore, RougeScore, NonLLMContextPrecisionWithReference
            _collection_metrics = True
        except ImportError:
            _collection_metrics = False

    RAGAS_AVAILABLE = True
except ImportError as e:
    _import_errors.append(str(e))
    RAGAS_AVAILABLE = False


def evaluate_response_quality(question: str, answer: str, contexts: List[str], openai_key: str = None) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""

    # Input validation - check for malformed inputs before processing
    if not isinstance(question, str) or not question.strip():
        return {"error": "Invalid input: 'question' must be a non-empty string"}

    if not isinstance(answer, str) or not answer.strip():
        return {"error": "Invalid input: 'answer' must be a non-empty string"}

    if contexts is None:
        return {"error": "Invalid input: 'contexts' cannot be None (use empty list [] if no context)"}

    if not isinstance(contexts, list):
        return {"error": "Invalid input: 'contexts' must be a list of strings"}

    if not RAGAS_AVAILABLE:
        return {"error": f"RAGAS not available - import errors: {'; '.join(_import_errors)}"}

    # Use Vocareum API key if not provided
    api_key = openai_key or os.getenv("OPENAI_API_KEY")
    base_url = "https://openai.vocareum.com/v1"

    # Create evaluator LLM
    evaluator_llm = LangchainLLMWrapper(
        ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=api_key,
            base_url=base_url
        )
    )

    # Create evaluator embeddings
    evaluator_embeddings = LangchainEmbeddingsWrapper(
        OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=api_key,
            base_url=base_url
        )
    )

    # Define metrics to evaluate
    metrics = []

    try:
        faithfulness_metric = Faithfulness()
        faithfulness_metric.llm = evaluator_llm
        metrics.append(faithfulness_metric)
    except Exception as e:
        pass

    try:
        relevancy_metric = ResponseRelevancy()
        relevancy_metric.llm = evaluator_llm
        relevancy_metric.embeddings = evaluator_embeddings
        metrics.append(relevancy_metric)
    except Exception as e:
        pass

    try:
        context_precision_metric = NonLLMContextPrecisionWithReference()
        metrics.append(context_precision_metric)
    except Exception:
        pass

    try:
        metrics.append(BleuScore())
        metrics.append(RougeScore())
    except Exception:
        pass

    if not metrics:
        return {"error": "No RAGAS metrics could be initialized"}

    # Create a sample
    sample = SingleTurnSample(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts if contexts else []
    )

    # Evaluate the response using the metrics (async)
    results = {}

    async def evaluate_metric(metric, sample):
        """Evaluate a single metric asynchronously"""
        metric_name = metric.__class__.__name__
        try:
            score = await metric.single_turn_ascore(sample)
            return metric_name, round(float(score), 4) if score is not None else 0.0, None
        except Exception as e:
            return metric_name, 0.0, str(e)

    async def run_all_metrics():
        """Run all metrics asynchronously"""
        tasks = [evaluate_metric(m, sample) for m in metrics]
        return await asyncio.gather(*tasks)

    # Run async evaluation
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context (like Streamlit), use nest_asyncio
            import nest_asyncio
            nest_asyncio.apply()
            scores = asyncio.run(run_all_metrics())
        else:
            scores = loop.run_until_complete(run_all_metrics())
    except RuntimeError:
        # No event loop running, create one
        scores = asyncio.run(run_all_metrics())

    for metric_name, score, error in scores:
        results[metric_name] = score
        if error:
            results[f"{metric_name}_error"] = error

    return results


