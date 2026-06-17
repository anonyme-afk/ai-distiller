"""
tools.py
Various tools available for agents.
"""
import logging

logger = logging.getLogger(__name__)

class MathCalculator:
    def calculate(self, expression: str) -> float:
        try:
            # ONLY use safe eval or specific parsing in real code
            # Note: eval is inherently unsafe, this is just a naive stub
            return float(eval(expression, {"__builtins__": None}, {}))
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return 0.0

class CodeSandbox:
    def execute(self, code: str) -> str:
        logger.warning("CodeSandbox execute called. In a real system this must run in Docker.")
        return "Executed securely in sandbox (stub)."
