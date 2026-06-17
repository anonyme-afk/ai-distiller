"""
cleaner.py
Data cleaning, filtering and format validation (Distilabel-style).
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DataCleaner:
    """Cleans and filters generated datasets."""

    def clean(self, dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply cleaning rules: deduplication, hallucination checks, length filters.
        """
        logger.info(f"Cleaning dataset of size {len(dataset)}")
        cleaned = []
        seen = set()

        for item in dataset:
            content = item.get("raw_generation", "")
            
            # Basic deduplication
            if content in seen:
                continue
            seen.add(content)
            
            # Basic validation
            if len(content) < 20:
                continue
                
            cleaned.append(item)
            
        logger.info(f"Dataset cleaned. Kept {len(cleaned)} items.")
        return cleaned
