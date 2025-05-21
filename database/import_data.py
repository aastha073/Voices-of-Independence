"""
Functions for importing data into Weaviate.
"""

import logging
from utils.opik_tracking import opik

logger = logging.getLogger(__name__)

@opik.track
def import_documents_to_weaviate(collection, documents, batch_size=10):
    """
    Import documents into Weaviate.
    
    Args:
        collection: Weaviate collection object
        documents (list): List of document dictionaries
        batch_size (int): Size of batches for import
        
    Returns:
        bool: True if import was successful
    """
    logger.info(f"Importing {len(documents)} documents into Weaviate...")
    
    try:
        # Import documents in batches
        with collection.batch.dynamic() as batch:
            for i, doc in enumerate(documents):
                properties = {
                    "text": doc["text"],
                    "title": doc["metadata"]["title"],
                    "date": doc["metadata"]["date"],
                    "authors": doc["metadata"]["authors"],
                    "document_type": doc["metadata"]["document_type"],
                    "source_url": doc["metadata"]["source_url"],
                    "chunk_id": doc["metadata"]["chunk_id"],
                    "total_chunks": doc["metadata"]["total_chunks"]
                }
                
                # Add recipient if it exists
                if "recipient" in doc["metadata"]:
                    properties["recipient"] = doc["metadata"]["recipient"]
                
                batch.add_object(
                    properties=properties,
                    uuid=None  # Let Weaviate generate a UUID
                )
                
                if (i + 1) % batch_size == 0 or i == len(documents) - 1:
                    logger.info(f"  Imported {i + 1}/{len(documents)} documents")
        
        logger.info("Import complete!")
        return True
        
    except Exception as e:
        logger.error(f"Error importing documents to Weaviate: {str(e)}")
        return False

@opik.track
def check_import_status(collection):
    """
    Check the status of the document import.
    
    Args:
        collection: Weaviate collection object
        
    Returns:
        dict: Import status information
    """
    try:
        # Get the object count in the collection
        object_count = collection.query.aggregate().with_meta_count().do()
        
        # Get a sample of documents to verify content
        sample = collection.query.get(
            properties=["title", "text"],
            limit=5
        )
        
        return {
            "object_count": object_count.total,
            "sample_docs": len(sample.objects),
            "status": "success" if object_count.total > 0 else "empty"
        }
        
    except Exception as e:
        logger.error(f"Error checking import status: {str(e)}")
        return {
            "object_count": 0,
            "sample_docs": 0,
            "status": "error",
            "error": str(e)
        }