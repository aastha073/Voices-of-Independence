"""
Weaviate client setup and connection management.
"""

import os
import logging
import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv
from utils.opik_tracking import opik

load_dotenv()
logger = logging.getLogger(__name__)

def get_weaviate_credentials():
    """Get Weaviate credentials from environment variables."""
    weaviate_url = os.getenv('WEAVIATE_CLUSTER_URL')
    weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
    friendli_token = os.getenv('FRIENDLI_TOKEN')
    
    if not weaviate_url or not weaviate_api_key:
        logger.error("Weaviate credentials not found in environment variables")
        raise ValueError("WEAVIATE_CLUSTER_URL and WEAVIATE_API_KEY must be set in environment variables")
    
    return {
        "url": weaviate_url,
        "api_key": weaviate_api_key,
        "friendli_token": friendli_token
    }

@opik.track
def connect_to_weaviate():
    """
    Connect to Weaviate cluster using credentials from environment variables.
    
    Returns:
        weaviate.Client: Connected Weaviate client
    """
    credentials = get_weaviate_credentials()
    
    headers = {}
    if credentials.get("friendli_token"):
        headers["X-Friendli-Token"] = credentials["friendli_token"]
    
    try:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=credentials["url"],
            auth_credentials=Auth.api_key(credentials["api_key"]),
            headers=headers
        )
        
        if client.is_connected():
            logger.info("Successfully connected to Weaviate")
            return client
        else:
            logger.error("Failed to connect to Weaviate")
            raise ConnectionError("Failed to connect to Weaviate")
    
    except Exception as e:
        logger.error(f"Error connecting to Weaviate: {str(e)}")
        raise
