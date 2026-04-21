"""
Batch Evaluation Script for NASA RAG System
Runs evaluation on test questions and outputs metric summaries
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List

import rag_client
import llm_client
import ragas_evaluator

def load_test_questions(file_path: str) -> List[Dict]:
    """Load test questions from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def run_batch_evaluation(questions: List[Dict], openai_key: str, 
                         chroma_dir: str, collection_name: str,
                         n_results: int = 3) -> Dict:
    """Run evaluation on all test questions"""
    
    # Initialize RAG system
    collection, success, error = rag_client.initialize_rag_system(chroma_dir, collection_name)
    if not success:
        return {"error": f"Failed to initialize RAG: {error}"}
    
    results = []
    all_metrics = {}
    
    for q in questions:
        # Retrieve documents
        docs = rag_client.retrieve_documents(collection, q["question"], n_results, openai_key=openai_key)
        
        if docs and docs.get("documents"):
            contexts = docs["documents"][0]
            context = rag_client.format_context(docs["documents"][0], docs["metadatas"][0])
        else:
            contexts = []
            context = ""
        
        # Generate response
        answer = llm_client.generate_response(openai_key, q["question"], context, [])
        
        # Evaluate
        metrics = ragas_evaluator.evaluate_response_quality(
            q["question"], answer, contexts, openai_key
        )
        
        # Store result
        result = {
            "id": q["id"],
            "category": q["category"],
            "mission": q["mission"],
            "question": q["question"],
            "answer": answer,
            "metrics": metrics
        }
        results.append(result)
        
        # Aggregate metrics
        for metric_name, value in metrics.items():
            if isinstance(value, (int, float)):
                if metric_name not in all_metrics:
                    all_metrics[metric_name] = []
                all_metrics[metric_name].append(value)
    
    # Calculate aggregate statistics
    aggregate = {}
    for metric_name, values in all_metrics.items():
        if values:
            aggregate[metric_name] = {
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "count": len(values)
            }
    
    return {
        "total_questions": len(questions),
        "results": results,
        "aggregate_metrics": aggregate
    }

def main():
    parser = argparse.ArgumentParser(description='Batch evaluation for NASA RAG')
    parser.add_argument('--test-questions', default='test_questions.json', help='Test questions file')
    parser.add_argument('--openai-key', required=True, help='OpenAI API key')
    parser.add_argument('--chroma-dir', default='./chroma_db_openai', help='ChromaDB directory')
    parser.add_argument('--collection', default='nasa_space_missions_text', help='Collection name')
    parser.add_argument('--output', default='evaluation_results.json', help='Output file')
    
    args = parser.parse_args()
    
    questions = load_test_questions(args.test_questions)
    print(f"Loaded {len(questions)} test questions")
    
    results = run_batch_evaluation(
        questions, args.openai_key, args.chroma_dir, args.collection
    )
    
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {args.output}")
    print("\nAggregate Metrics:")
    for metric, stats in results.get("aggregate_metrics", {}).items():
        print(f"  {metric}: mean={stats['mean']:.3f}, min={stats['min']:.3f}, max={stats['max']:.3f}")

if __name__ == "__main__":
    main()