from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional
import os

# RAGAS imports
try:
    from ragas import SingleTurnSample
    from ragas.metrics.collections import BleuScore, NonLLMContextPrecisionWithReference, RougeScore
    from ragas.metrics import ResponseRelevancy, Faithfulness
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

def evaluate_response_quality(question: str, answer: str, contexts: List[str], openai_key: str = None) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}
    
    # TODO: Create evaluator LLM with model gpt-3.5-turbo
    api_key = openai_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OpenAI API key not provided"}
    evaluator_llm = LangchainLLMWrapper(
        model=ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=api_key,
            base_url="https://openai.vocareum.com/v1"
        )
    )
    
    # TODO: Create evaluator_embeddings with model text-embedding-3-small
    evaluator_embeddings = LangchainEmbeddingsWrapper(
        model=OpenAIEmbeddings(
            model_name="text-embedding-3-small",
            openai_api_key=api_key,
            base_url="https://openai.vocareum.com/v1"
        )
    )
    
    # TODO: Define an instance for each metric to evaluate
    metrics = [
        BleuScore(),
        NonLLMContextPrecisionWithReference(),
        ResponseRelevancy(),
        Faithfulness(),
        RougeScore()
    ]
    
    # create a sample
    sample = SingleTurnSample(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts
    )
    
    # TODO: Evaluate the response using the metrics
    results = {}

    for metric in metrics:
        try:
            # Set the LLM and embeddings for metrics that need them
            if hasattr(metric, 'llm'):
                metric.llm = evaluator_llm
            if hasattr(metric, 'embeddings'):
                metric.embeddings = evaluator_embeddings

            # Calculate the metric score
            score = metric.score(sample)
            metric_name = metric.__class__.__name__
            results[metric_name] = score
        except Exception as e:
            # Return the evaluation results even if some metrics fail
            results[metric.__class__.__name__] = 0.0
            results[f"{metric.__class__.__name__}_error"] = str(e)
    
    # TODO: Return the evaluation results
    return results

