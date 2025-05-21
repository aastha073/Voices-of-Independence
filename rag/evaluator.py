"""
Evaluation functions for the RAG system.
"""

import logging
from utils.opik_tracking import opik
from .generator import get_friendli_client, call_llm
from .retriever import prepare_context_for_llm

logger = logging.getLogger(__name__)

@opik.track
def evaluate_retrieval_quality(query, retrieved_docs):
    """
    Evaluate the quality of retrieved documents.
    
    Args:
        query (str): User query
        retrieved_docs (list): Retrieved documents
        
    Returns:
        str: Evaluation result
    """
    client = get_friendli_client()
    
    # Create messages for the LLM to evaluate retrieval quality
    eval_prompt = f"""
    Given the user query: "{query}"
    
    And these retrieved documents:
    {prepare_context_for_llm(retrieved_docs)}
    
    Please evaluate the retrieval quality by answering these questions:
    1. On a scale of 1-10, how relevant are the retrieved documents to the query?
    2. Which document is most relevant to the query and why?
    3. Are there any retrieved documents that seem irrelevant?
    4. What related documents or information might be missing?
    
    Provide your evaluation in this format:
    RELEVANCE_SCORE: [1-10]
    MOST_RELEVANT: [document title]
    IRRELEVANT_DOCS: [list or "None"]
    MISSING_INFO: [description]
    """
    
    messages = [
        {"role": "system", "content": "You are an AI assistant that evaluates search result quality for historical document retrieval."},
        {"role": "user", "content": eval_prompt}
    ]
    
    response = call_llm(client, messages)
    return response.choices[0].message.content

@opik.track
def evaluate_response_quality(query, context, response):
    """
    Evaluate the quality of the generated response.
    
    Args:
        query (str): User query
        context (str): Context provided to the LLM
        response (str): Generated response
        
    Returns:
        str: Evaluation result
    """
    client = get_friendli_client()
    
    # Create messages for the LLM to evaluate response quality
    eval_prompt = f"""
    Given the user query: "{query}"
    
    The context provided to the AI:
    {context}
    
    And the AI's response:
    {response}
    
    Please evaluate the response quality by answering these questions:
    1. On a scale of 1-10, how well does the response answer the query?
    2. Does the response accurately reflect the information in the context?
    3. Is there any hallucination or information not supported by the context?
    4. How could the response be improved?
    
    Provide your evaluation in this format:
    RESPONSE_QUALITY: [1-10]
    ACCURACY: [1-10]
    HALLUCINATION: [Yes/No with explanation]
    IMPROVEMENTS: [suggestions]
    """
    
    messages = [
        {"role": "system", "content": "You are an AI assistant that evaluates response quality for historical document retrieval and synthesis."},
        {"role": "user", "content": eval_prompt}
    ]
    
    response = call_llm(client, messages)
    return response.choices[0].message.content

@opik.track(name="evaluate-rag-system")
def evaluate_rag_system(collection, query, response, context, formatted_results):
    """
    Perform a complete evaluation of the RAG system for a given query.
    
    Args:
        collection: Weaviate collection
        query (str): User query
        response (str): Generated response
        context (str): Context provided to the LLM
        formatted_results (list): Formatted search results
        
    Returns:
        dict: Evaluation results
    """
    # Evaluate retrieval quality
    retrieval_eval = evaluate_retrieval_quality(query, formatted_results)
    
    # Evaluate response quality
    response_eval = evaluate_response_quality(query, context, response)
    
    return {
        "query": query,
        "retrieval_evaluation": retrieval_eval,
        "response_evaluation": response_eval
    }