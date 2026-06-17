"""Tests for distillation module."""
import pytest
from ai_distiller.distillation.cleaner import DataCleaner
from ai_distiller.distillation.data_generator import DataGenerator
from unittest.mock import MagicMock

def test_data_cleaner():
    """Test the DataCleaner logic."""
    cleaner = DataCleaner()
    raw_data = [
        {"input": "Hello", "output": "World"},
        {"input": "Hello", "output": "World"},  # Duplicate
        {"input": "Short", "output": "Hi"},     # Too short (if we had length limits, stub for now)
        {"input": "Valid input", "output": "This is a valid response that should be kept."}
    ]
    
    # Assuming cleaner deduplicates
    cleaned = cleaner.clean(raw_data)
    
    assert len(cleaned) < len(raw_data)
    assert cleaned[0]["instruction"] == "Hello" # checks formatting to alpaca/sharegpt
    assert "input" not in cleaned[0]

def test_data_generator(mocker):
    """Test DataGenerator with a mocked TeacherConnector."""
    mock_teacher = MagicMock()
    mock_teacher.generate.return_value = '{"input": "Mock input", "output": "Mock output"}'
    
    generator = DataGenerator(teacher=mock_teacher)
    dataset = generator.generate(domain="test_domain", num_examples=2)
    
    assert len(dataset) == 2
    assert dataset[0] == '{"input": "Mock input", "output": "Mock output"}'
    mock_teacher.generate.assert_called()
