import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Set up logging configuration for the application"""

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        'qdrant_rag_validation.log',
        maxBytes=1024*1024*5,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Initialize the logger
logger = setup_logging()