"""
Weaviate schema definition for historical documents.
"""

import logging
import weaviate
from utils.opik_tracking import opik

logger = logging.getLogger(__name__)

COLLECTION_NAME = "HistoricalDocuments"

@opik.track
def setup_weaviate_schema(client, recreate=False):
    """
    Set up the Weaviate schema for historical documents.
    
    Args:
        client: Weaviate client
        recreate (bool): Whether to recreate the collection if it exists
        
    Returns:
        collection: The Weaviate collection object
    """
    # Check if collection already exists
    collections = client.collections.list_all()
    collection_names = [c.name for c in collections]
    
    if COLLECTION_NAME in collection_names:
        if recreate:
            logger.info(f"{COLLECTION_NAME} collection already exists. Deleting it to recreate...")
            client.collections.delete(COLLECTION_NAME)
        else:
            logger.info(f"{COLLECTION_NAME} collection already exists. Using existing collection.")
            return client.collections.get(COLLECTION_NAME)
    
    # Define the schema for our collection
    historical_docs = client.collections.create(
        name=COLLECTION_NAME,
        description="Historical documents from the American Revolution and founding era",
        vectorizer_config=weaviate.classes.config.Configure.Vectorizer.text2vec_transformers(),
        properties=[
            weaviate.classes.config.Property(
                name="text",
                data_type=weaviate.classes.config.DataType.TEXT,
                description="The text content of the document chunk",
                skip_vectorization=False,
                tokenization=weaviate.classes.config.Configure.Tokenization.field()
            ),
            weaviate.classes.config.Property(
                name="title",
                data_type=weaviate.classes.config.DataType.TEXT,
                description="The title of the document",
                skip_vectorization=False,
                tokenization=weaviate.classes.config.Configure.Tokenization.word()
            ),
            weaviate.classes.config.Property(
                name="date",
                data_type=weaviate.classes.config.DataType.DATE,
                description="The date the document was written",
                skip_vectorization=True
            ),
            weaviate.classes.config.Property(
                name="authors",
                data_type=weaviate.classes.config.DataType.TEXT_ARRAY,
                description="The authors of the document",
                skip_vectorization=False,
                tokenization=weaviate.classes.config.Configure.Tokenization.word()
            ),
            weaviate.classes.config.Property(
                name="document_type",
                data_type=weaviate.classes.config.DataType.TEXT,
                description="The type of document (letter, speech, founding_document, etc.)",
                skip_vectorization=False,
                tokenization=weaviate.classes.config.Configure.Tokenization.word()
            ),
            weaviate.classes.config.Property(
                name="source_url",
                data_type=weaviate.classes.config.DataType.TEXT,
                description="The URL where the document was sourced",
                skip_vectorization=True
            ),
            weaviate.classes.config.Property(
                name="chunk_id",
                data_type=weaviate.classes.config.DataType.INT,
                description="The ID of this chunk within the document",
                skip_vectorization=True
            ),
            weaviate.classes.config.Property(
                name="total_chunks",
                data_type=weaviate.classes.config.DataType.INT,
                description="The total number of chunks in the document",
                skip_vectorization=True
            ),
            weaviate.classes.config.Property(
                name="recipient",
                data_type=weaviate.classes.config.DataType.TEXT,
                description="The recipient of the document (for letters)",
                skip_vectorization=False,
                tokenization=weaviate.classes.config.Configure.Tokenization.word()
            )
        ]
    )
    
    logger.info(f"Created {COLLECTION_NAME} collection")
    return historical_docs

def get_collection(client):
    """Get the HistoricalDocuments collection."""
    try:
        return client.collections.get(COLLECTION_NAME)
    except Exception as e:
        logger.error(f"Error getting collection {COLLECTION_NAME}: {str(e)}")
        return None