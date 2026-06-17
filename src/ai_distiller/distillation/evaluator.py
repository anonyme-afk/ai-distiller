"""
evaluator.py
LLM-as-a-Judge benchmarking for the distilled model against the Teacher.
"""
import logging
import asyncio
from typing import List, Dict, Any
from .teacher import TeacherConnector

logger = logging.getLogger(__name__)

class Evaluator:
    """Benchmarks a student model by comparing its answers to the teacher."""

    def __init__(self, teacher: TeacherConnector):
        self.judge = teacher

    async def _evaluate_single(self, prompt: str, student_answer: str, teacher_answer: str) -> float:
        """Uses the judge to rate the student answer compared to the teacher's (0.0 to 10.0)."""
        evaluation_prompt = (
            f"Prompt: {prompt}\n\n"
            f"Teacher Answer (Reference):\n{teacher_answer}\n\n"
            f"Student Answer:\n{student_answer}\n\n"
            "Rate the Student Answer from 0 to 10 based on how well it captures the accuracy and quality of the Teacher Answer. "
            "Output ONLY the numerical score."
        )
        
        try:
            score_str = await self.judge.generate_async(evaluation_prompt)
            # Extremely naive parsing for POC
            import re
            numbers = re.findall(r"\d+\.?\d*", score_str)
            if numbers:
                return min(10.0, float(numbers[0]))
            return 5.0
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return 0.0

    async def benchmark_async(self, test_set: List[Dict[str, str]]) -> Dict[str, Any]:
        """Runs the benchmark concurrently on the holdout test set."""
        logger.info(f"Running LLM-as-a-Judge benchmark on {len(test_set)} examples...")
        
        tasks = []
        for item in test_set:
            tasks.append(self._evaluate_single(item["prompt"], item["student_answer"], item["teacher_answer"]))
            
        scores = await asyncio.gather(*tasks)
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        logger.info(f"Benchmark Complete! Average Score: {avg_score:.2f}/10")
        return {
            "average_score": avg_score,
            "individual_scores": scores
        }

    def benchmark(self, test_set: List[Dict[str, str]]) -> Dict[str, Any]:
        """Synchronous wrapper."""
        return asyncio.run(self.benchmark_async(test_set))
