"""
data_generator.py
Async generation of training data (DPO format) using Constitutional AI approach.
"""
import logging
import asyncio
from typing import List, Dict, Any
from .teacher import TeacherConnector

logger = logging.getLogger(__name__)

class DataGenerator:
    """Generates synthetic DPO dataset from a teacher model."""

    def __init__(self, teacher: TeacherConnector):
        self.teacher = teacher

    async def _generate_single_dpo_example(self, domain: str, with_cot: bool) -> Dict[str, str]:
        system_prompt = f"You are a master dataset creator for an AI assistant specialized in {domain}."
        prompt_generation = f"Generate a realistic, difficult user request/prompt for the domain: {domain}. Output ONLY the prompt text, nothing else."
        
        # Step 1: Generate the prompt
        user_prompt = await self.teacher.generate_async(prompt_generation, system=system_prompt)
        
        # Step 2: Generate N diverse responses (Rejection Sampling)
        if with_cot:
            sys_instruct = "Include a <thinking> process before your final answer."
        else:
            sys_instruct = None
            
        candidate_responses = await self.teacher.generate_n_async(user_prompt, n=3, system=sys_instruct)
        
        # Step 3: LLM-as-a-Judge to pick chosen/rejected
        chosen, rejected = await self.teacher.evaluate_responses(user_prompt, candidate_responses)
        
        return {
            "prompt": user_prompt,
            "chosen": chosen,
            "rejected": rejected
        }

    async def generate_async(self, domain: str, num_examples: int = 10, with_cot: bool = False) -> List[Dict[str, str]]:
        """Asynchronously generate DPO examples concurrently."""
        logger.info(f"Generating {num_examples} DPO examples for domain: {domain} concurrently.")
        tasks = [self._generate_single_dpo_example(domain, with_cot) for _ in range(num_examples)]
        # Gather all concurrent tasks
        dataset = await asyncio.gather(*tasks)
        return list(dataset)

    def generate(self, domain: str, num_examples: int = 10, with_cot: bool = False) -> List[Dict[str, str]]:
        """Synchronous wrapper for CLI legacy compatibility."""
        return asyncio.run(self.generate_async(domain, num_examples, with_cot))
