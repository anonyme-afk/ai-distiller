"""
rag.py
RAG integration with LlamaIndex.
"""
import logging
from pathlib import Path
try:
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
except ImportError:
    VectorStoreIndex = None
    SimpleDirectoryReader = None

logger = logging.getLogger(__name__)

class RAGIntegration:
    """Retrieval-Augmented Generation using LlamaIndex."""

    def __init__(self, index_dir: str = "./index"):
        self.index_dir = index_dir
        self.index = None
        self.documents = []

    def load_documents(self, data_source_paths: list[str]):
        logger.info(f"Loading documents from {len(data_source_paths)} sources.")
        if SimpleDirectoryReader is None:
            logger.warning("llama-index is not installed. Returning stub.")
            return

        for path in data_source_paths:
            if Path(path).exists() and Path(path).is_file():
                self.documents.extend(SimpleDirectoryReader(input_files=[path]).load_data())
            elif Path(path).exists() and Path(path).is_dir():
                self.documents.extend(SimpleDirectoryReader(input_dir=path).load_data())
            else:
                logger.warning(f"Path not found: {path}")

    def build_index(self):
        logger.info("Building vector index.")
        if VectorStoreIndex is None:
            return
        if self.documents:
            self.index = VectorStoreIndex.from_documents(self.documents)

    def query(self, query_str: str) -> str:
        logger.info(f"Querying index: {query_str}")
        if self.index is None:
            return "RAG engine not initialized or index is empty."
        
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query_str)
        return str(response)
