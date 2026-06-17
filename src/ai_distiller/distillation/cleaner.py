"""
cleaner.py
Data cleaning, filtering and format validation for DPO and SFT datasets.

Integrates with:
- Distilabel: https://github.com/argilla-io/distilabel (inspiration for filtering)
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DataCleaner:
    """Cleans and filters generated datasets (supports DPO and SFT formats)."""

    def __init__(self, min_length: int = 20):
        self.min_length = min_length

    def clean(self, dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply cleaning rules: deduplication, length filters, format normalization.
        Supports both DPO format (prompt/chosen/rejected) and legacy (raw_generation).
        """
        logger.info(f"Cleaning dataset of size {len(dataset)}")
        cleaned = []
        seen = set()

        for item in dataset:
            # DPO format
            if "prompt" in item and "chosen" in item:
                content_key = item["prompt"] + item["chosen"]
                if content_key in seen:
                    continue
                seen.add(content_key)

                if len(item.get("chosen", "")) < self.min_length:
                    continue

                cleaned.append({
                    "prompt": item["prompt"].strip(),
                    "chosen": item["chosen"].strip(),
                    "rejected": item.get("rejected", "").strip(),
                })

            # Legacy SFT format (input/output or raw_generation)
            elif "input" in item and "output" in item:
                content_key = item["input"] + item["output"]
                if content_key in seen:
                    continue
                seen.add(content_key)

                if len(item.get("output", "")) < self.min_length:
                    continue

                cleaned.append({
                    "instruction": item["input"].strip(),
                    "output": item["output"].strip(),
                })

            elif "raw_generation" in item:
                content = item["raw_generation"]
                if content in seen:
                    continue
                seen.add(content)
                if len(content) < self.min_length:
                    continue
                cleaned.append({"instruction": content.strip(), "output": ""})

        logger.info(f"Dataset cleaned. Kept {len(cleaned)}/{len(dataset)} items.")
        return cleaned
