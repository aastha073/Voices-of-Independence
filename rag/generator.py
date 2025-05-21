"""
Response generation functions for the RAG system.
"""

import os
import logging
from openai import OpenAI
from utils.opik_tracking import opik

logger = logging.getLogger(__name__)

# Set up FriendliAI client
def get_friendli_client():
    """Get FriendliAI client."""
    friendli_token = os.getenv('FRIENDLI_TOKEN')
    if not friendli_token:
        raise ValueError("FRIENDLI_TOKEN environment variable is not set")
    
    return OpenAI(
        base_url="https://api.friendli.ai/serverless/v1",
        api_key=friendli_token
    )

@opik.track
def call_llm(client, messages, model="meta-llama-3.3-70b-instruct"):
    """
    Call the LLM through FriendliAI.
    
    Args:
        client: OpenAI-compatible client
        messages (list): Messages for the chat completion
        model (str): Model identifier
        
    Returns:
        response: LLM response
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response
    except Exception as e:
        logger.error(f"Error calling LLM: {str(e)}")
        raise

@opik.track
def get_system_prompt(mode="historian"):
    """
    Get system prompt based on response mode.
    
    Args:
        mode (str): Response mode
        
    Returns:
        str: System prompt
    """
    if mode == "historian":
        return """
        You are an expert historian specializing in American Independence and the Revolutionary period.
        Answer questions about this time period using the provided historical documents as reference.
        Support your statements with evidence from the documents, citing the document title and date where appropriate.
        If the documents don't contain information to answer the question, acknowledge this and provide
        general historical context based on your knowledge.
        """
    elif mode == "founding_father":
        return """
        You are Benjamin Franklin, a Founding Father of the United States.
        You're speaking from the perspective of someone who lived during the American Revolution and
        helped draft the Declaration of Independence.
        Use a formal, eloquent speaking style appropriate for an educated 18th-century statesman.
        Base your responses on the historical context provided, but speak as if these are your personal
        memories and experiences. This means using first-person pronouns when appropriate.
        """
    elif mode == "time_traveler":
        return """
        You are a time-traveling guide from 2025 taking people on an educational journey back to Revolutionary America.
        Your goal is to make history accessible and exciting, drawing connections between the past and present.
        Use the provided historical context to educate visitors about the formation of the United States,
        but frame it in an engaging, conversational way that helps modern people understand the significance.
        """
    else:  # Default response mode
        return """
        You are an AI assistant helping users learn about American history.
        Answer questions about American Independence and the Revolutionary period using the
        provided historical documents as reference.
        """

@opik.track
def generate_response(query, context, mode="historian"):
    """
    Generate a response using the LLM based on the retrieved context.
    
    Args:
        query (str): User query
        context (str): Retrieved context
        mode (str): Response mode
        
    Returns:
        str: Generated response
    """
    client = get_friendli_client()
    system_message = get_system_prompt(mode)
    
    # Create messages for the LLM
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Here are some relevant historical documents:\n\n{context}\n\nBased on these documents, please answer: {query}"}
    ]
    
    # Call the LLM
    logger.info(f"Generating response in '{mode}' mode")
    response = call_llm(client, messages)
    
    return response.choices[0].message.content