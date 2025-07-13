import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Log file path
log_file = os.path.join(logs_dir, "mcp_actions.log")

def configure_logging(logger_name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Configure logging with both console and file output.
    
    Args:
        logger_name: Name of the logger
        level: Logging level (default: DEBUG)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    
    # Clear any existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create formatters
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    
    # Create file handler (10MB max size, keep 5 backup files)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def get_action_logger(action_name: str, parent_logger_name: Optional[str] = None) -> logging.Logger:
    """Get a logger for a specific MCP action with proper formatting.
    
    Args:
        action_name: Name of the action
        parent_logger_name: Name of the parent logger (optional)
        
    Returns:
        Logger instance for the action
    """
    if parent_logger_name:
        logger_name = f"{parent_logger_name}.{action_name}"
    else:
        logger_name = f"mcp_action.{action_name}"
    
    logger = logging.getLogger(logger_name)
    
    # If this is the first time getting this logger, configure it
    if not logger.handlers:
        # Create formatters
        file_formatter = logging.Formatter('%(asctime)s - ACTION[%(name)s] - %(levelname)s - %(message)s')
        
        # Create file handler (10MB max size, keep 5 backup files)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Add handler to logger
        logger.addHandler(file_handler)
    
    return logger
