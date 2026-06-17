from pathlib import Path
from setuptools import find_packages, setup

this_dir = Path(__file__).parent
readme = this_dir / "README.md"
long_description = readme.read_text(encoding="utf-8") if readme.exists() else ""

setup(
    name="ai-distiller",
    version="0.1.0",
    description="Build specialized AI assistants via model distillation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.5.0",
        "pydantic-settings>=2.2.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "typer>=0.12.0",
        "rich>=13.7.0",
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.27.0",
    ],
    extras_require={
        "anthropic": ["anthropic>=0.39.0"],
        "openai": ["openai>=1.40.0"],
        "orchestration": ["langgraph>=0.0.40", "langchain>=0.2.0", "crewai>=0.30.0"],
        "rag": ["llama-index>=0.10.0"],
        "search": ["tavily-python>=0.3.0", "duckduckgo-search>=5.0.0"],
        "training": ["torch>=2.0.0", "transformers>=4.35.0", "datasets>=2.14.0", "huggingface-hub>=0.19.0"],
        "dev": ["pytest>=8.0.0", "pytest-asyncio>=0.23.0"],
    },
    entry_points={
        "console_scripts": [
            "ai-distiller=ai_distiller.cli.main:app",
        ],
    },
)
