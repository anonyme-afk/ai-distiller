"""Exemple avec CrewAI"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ai_distiller.orchestration.crew_builder import CrewBuilder

# Création de l'équipe
crew = CrewBuilder()\
    .add_agent("Analyzer", tools=["sentiment"])\
    .add_agent("Researcher", tools=["rag"])\
    .add_agent("Writer")\
    .add_validator(teacher="claude-3-5-sonnet")\
    .build()

# Utilisation
result = crew.process("Ticket client : Ma commande est cassée")
print(result)
