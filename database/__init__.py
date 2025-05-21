"""
Database module for Weaviate vector database operations.
"""

from .weaviate_client import connect_to_weaviate
from .schema import setup_weaviate_schema, get_collection, COLLECTION