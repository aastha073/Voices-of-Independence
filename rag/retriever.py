"""
Document retrieval functions for the RAG system.
"""

import logging
from utils.opik_tracking import opik

logger = logging.getLogger(__name__)

@opik.track
def search_historical_documents(collection, query, limit=5):
    """
    Search for historical documents relevant to the query.
    
    Args:
        collection: Weaviate collection
        query (str): User query
        limit (int): Maximum number of results
        
    Returns:
        list: Search results
    """
    logger.info(f"Searching for: {query}")
    
    try:
        results = collection.query.near_text(
            query=query,
            limit=limit
        )
        
        logger.info(f"Found {len(results.objects)} relevant documents")
        return results.objects
    
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        return []

@opik.track
def format_search_results(results):
    """
    Format search results for display and LLM context.
    
    Args:
        results (list): Raw search results
        
    Returns:
        list: Formatted results
    """
    formatted_results = []
    
    for result in results:
        doc = {
            "text": result.properties["text"],
            "title": result.properties["title"],
            "date": result.properties["date"],
            "authors": ", ".join(result.properties["authors"]),
            "document_type": result.properties["document_type"],
            "chunk_id": result.properties.get("chunk_id", 0),
            "total_chunks": result.properties.get("total_chunks", 1)
        }
        
        # Add recipient for letters
        if "recipient" in result.properties:
            doc["recipient"] = result.properties["recipient"]
        
        formatted_results.append(doc)
    
    return formatted_results

@opik.track
def prepare_context_for_llm(formatted_results):
    """
    Prepare context from search results for the LLM.
    
    Args:
        formatted_results (list): Formatted search results
        
    Returns:
        str: Context text for LLM prompt
    """
    context = ""
    
    for i, doc in enumerate(formatted_results):
        context += f"\n\nDOCUMENT {i+1}:\n"
        context += f"Title: {doc['title']}\n"
        context += f"Date: {doc['date']}\n"
        context += f"Author(s): {doc['authors']}\n"
        context += f"Type: {doc['document_type']}\n"
        
        if "recipient" in doc:
            context += f"Recipient: {doc['recipient']}\n"
        
        context += f"Chunk: {doc['chunk_id']+1} of {doc['total_chunks']}\n"
        context += f"Content:\n{doc['text']}\n"
    
    return context

@opik.track(name="retrieve-context")
def retrieve_context(collection, query, limit=5):
    """
    Retrieve context relevant to the user's query.
    
    Args:
        collection: Weaviate collection
        query (str): User query
        limit (int): Maximum number of results
        
    Returns:
        dict: Retrieved context and metadata
    """
    # Search for relevant documents
    results = search_historical_documents(collection, query, limit=limit)
    
    # Format results
    formatted_results = format_search_results(results)
    
    # Prepare context for LLM
    context = prepare_context_for_llm(formatted_results)
    
    return {
        "context": context,
        "formatted_results": formatted_results,
        "raw_results": results
    }
