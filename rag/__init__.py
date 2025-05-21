"""
RAG module for the Voices of Independence project.
Provides the retrieval-augmented generation system for answering
questions about American Independence.
"""

from .retriever import (
    search_historical_documents,
    format_search_results,
    prepare_context_for_llm,
    retrieve_context
)
from .generator import (
    get_friendli_client,
    call_llm,
    get_system_prompt,
    generate_response
)
from .evaluator import (
    evaluate_retrieval_quality,
    evaluate_response_quality,
    evaluate_rag_system
)
from .independence_rag import independence_rag

__all__ = [
    'search_historical_documents',
    'format_search_results',
    'prepare_context_for_llm',
    'retrieve_context',
    'get_friendli_client',
    'call_llm',
    'get_system_prompt',
    'generate_response',
    'evaluate_retrieval_quality',
    'evaluate_response_quality',
    'evaluate_rag_system',
    'independence_rag'
]