# API Reference

*Note: This section is generated from docstrings. Below are the primary classes.*

### `TeacherConnector`
**Path**: `ai_distiller.distillation.teacher.TeacherConnector`

Connects to a teacher model.
```python
teacher = TeacherConnector(provider="anthropic", model="claude-3-5-sonnet-20241022")
response = teacher.generate("Explain distillation.")
```

### `DataGenerator`
**Path**: `ai_distiller.distillation.data_generator.DataGenerator`

Generates synthetic data given a domain configuration.
```python
generator = DataGenerator(teacher)
dataset = generator.generate("support_client", 100)
```
