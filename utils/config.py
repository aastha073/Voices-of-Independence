"""
Configuration management for the application.
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "response_modes": {
        "historian": "Expert Historian",
        "founding_father": "Benjamin Franklin (Role Play)",
        "time_traveler": "Time-Traveling Guide"
    },
    "default_mode": "historian",
    "default_search_limit": 5,
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "batch_size": 10
}

def get_config():
    """
    Get application configuration from environment variables.
    
    Returns:
        dict: Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    # Override defaults with environment variables
    config["default_mode"] = os.getenv('DEFAULT_RESPONSE_MODE', config["default_mode"])
    config["default_search_limit"] = int(os.getenv('DEFAULT_SEARCH_LIMIT', config["default_search_limit"]))
    
    return config

def configure_logging():
    """Configure application logging."""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Reduce logging from some verbose libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    logger.info(f"Logging configured at {log_level} level")