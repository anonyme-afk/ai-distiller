"""Exemple simple de distillation"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ai_distiller.distillation.teacher import TeacherConnector
from ai_distiller.distillation.data_generator import DataGenerator
from ai_distiller.distillation.cleaner import DataCleaner
from ai_distiller.distillation.trainer import Trainer

# Initialize
teacher = TeacherConnector()
generator = DataGenerator(teacher)
cleaner = DataCleaner()
trainer = Trainer()

# Génération
dataset = generator.generate(domain="support_client", num_examples=5)

# Nettoyage
cleaned = cleaner.clean(dataset)

# Entraînement
result = trainer.train(cleaned)

print("Distillation complete. Model saved at:", result["model_path"])
