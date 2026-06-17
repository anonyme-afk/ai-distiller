"""
data_generator.py
Generation of training data using the teacher model (Magpie-style).
"""
import logging
from typing import List, Dict, Any
from .teacher import TeacherConnector

logger = logging.getLogger(__name__)

class DataGenerator:
    """Generates synthetic dataset from a teacher model."""

    def __init__(self, teacher: TeacherConnector):
        self.teacher = teacher

    def generate(self, domain: str, num_examples: int = 10, with_cot: bool = False) -> List[Dict[str, str]]:
        """Generate a list of examples (prompt and response)."""
        logger.info(f"Generating {num_examples} examples for domain: {domain}")
        dataset = []
        
        system_prompt = f"You are generating training data for an AI assistant specialized in {domain}."
        
        for i in range(num_examples):
            # This is a simplified generation loop. In a real Magpie approach, 
            # we would use varied prompt templates or seed questions.
            generation_prompt = f"Generate a realistic user request for the domain: {domain}. Then, provide the perfect response."
            if with_cot:
                generation_prompt += " Include a <thinking> process before the final response."

            response = self.teacher.complete(generation_prompt, system=system_prompt)
            
            # Simple parsing: assume the teacher output format is "User: ... \n\nAssistant: ..."
            # For this MVP, we just store the raw generation.
            dataset.append({
                "raw_generation": response
            })
            
        return dataset
