"""Exemple pipeline complet"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ai_distiller.cli.main import app

print("Use the CLI to run the full pipeline:")
print("python -m ai_distiller.cli.main wizard")
