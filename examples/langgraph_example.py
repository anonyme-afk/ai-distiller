"""Exemple avec LangGraph"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ai_distiller.orchestration.langgraph_builder import LangGraphBuilder

graph = LangGraphBuilder()\
    .add_node("search", lambda state: state)\
    .add_node("verify", lambda state: state)\
    .add_edge("search", "verify")\
    .build()

result = graph.invoke({"query": "Droit civil"})
print(result)
