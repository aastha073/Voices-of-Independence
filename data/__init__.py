"""
Data module for the Voices of Independence project.
Provides functionality for collecting and processing historical documents.
"""

from .sources import SOURCES, get_all_sources, get_sources_by_type
from .document_fetcher import fetch_document
from .document_processor import chunk_text, process_document, collect_all_documents

__all__ = [
    'SOURCES',
    'get_all_sources',
    'get_sources_by_type',
    'fetch_document',
    'chunk_text',
    'process_document',
    'collect_all_documents'
]