"""
logger.py
Centralized logging configuration for AI-Distiller.
"""
import logging
from rich.logging import RichHandler
from pathlib import Path

def setup_logger(log_level=logging.INFO, log_file="ai-distiller.log"):
    """
    Configures the root logger with a Rich handler for the console
    and a File handler for persistence.
    """
    # Create logs directory if it doesn't exist
    log_path = Path("outputs")
    log_path.mkdir(parents=True, exist_ok=True)
    full_log_path = log_path / log_file

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(rich_tracebacks=True, markup=True),
            logging.FileHandler(full_log_path, encoding="utf-8")
        ]
    )
    
    # Get the specific logger for our package to avoid polluting third-party logs
    logger = logging.getLogger("ai_distiller")
    logger.setLevel(log_level)
    return logger

# Create a default logger instance
logger = setup_logger()
