"""
Main RAG pipeline for the Voices of Independence project.
"""

import logging
from utils.opik_tracking import opik
from .retriever import retrieve_context
from .generator import generate_response
from .evaluator import evaluate_rag_system

logger = logging.getLogger(__name__)

@opik.track(name="independence-rag")
def independence_rag(collection, query, mode="historian", limit=5, evaluate=False):
    """
    Complete RAG pipeline for answering questions about American Independence.
    
    Args:
        collection: Weaviate collection
        query (str): User query
        mode (str): Response mode (historian, founding_father, time_traveler)
        limit (int): Maximum number of documents to retrieve
        evaluate (bool): Whether to evaluate the response
        
    Returns:
        dict: RAG results including query, response, and sources
    """
    logger.info(f"Processing query: '{query}' in mode: '{mode}'")
    
    # Retrieve context
    retrieved_info = retrieve_context(collection, query, limit=limit)
    context = retrieved_info["context"]
    formatted_results = retrieved_info["formatted_results"]
    
    # Generate response
    response = generate_response(query, context, mode=mode)
    
    # Prepare result
    result = {
        "query": query,
        "response": response,
        "context": context,
        "mode": mode,
        "sources": [doc["title"] for doc in formatted_results]
    }
    
    # Evaluate if requested
    if evaluate:
        logger.info("Evaluating RAG response")
        evaluation = evaluate_rag_system(
            collection, 
            query, 
            response, 
            context, 
            formatted_results
        )
        result["evaluation"] = evaluation
    
    return result