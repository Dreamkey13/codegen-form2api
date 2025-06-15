import pytest
import os
import logging
from src.config.logging import setup_logging

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up the test environment."""
    # Set up logging
    setup_logging(log_level=logging.DEBUG)
    
    # Create necessary directories
    os.makedirs("templates", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    yield
    
    # Cleanup after tests
    # Add cleanup code if needed

@pytest.fixture
def sample_form_data():
    """Provide sample form data for testing."""
    return [
        {
            "id": "field1",
            "name": "field1",
            "type": "text",
            "required": "true",
            "pattern": "[A-Za-z]+"
        },
        {
            "id": "field2",
            "name": "field2",
            "type": "number",
            "min": "0",
            "max": "100"
        },
        {
            "id": "field3",
            "name": "field3",
            "type": "select",
            "options": [
                {"value": "1", "text": "Option 1"},
                {"value": "2", "text": "Option 2"}
            ]
        }
    ]

@pytest.fixture
def sample_analyzed_data():
    """Provide sample analyzed form data for testing."""
    return [
        {
            "id": "field1",
            "name": "field1",
            "type": "text",
            "validation_rules": ["required", "pattern"],
            "events": ["onchange"],
            "is_postback": False
        },
        {
            "id": "field2",
            "name": "field2",
            "type": "number",
            "validation_rules": ["min", "max"],
            "events": [],
            "is_postback": False
        },
        {
            "id": "field3",
            "name": "field3",
            "type": "select",
            "validation_rules": [],
            "events": ["onchange"],
            "is_postback": False
        }
    ]

@pytest.fixture
def sample_generation_request():
    """Provide sample code generation request data."""
    return {
        "url": "https://example.com",
        "platform": "test-platform",
        "form_name": "test-form",
        "language": "python",
        "username": "testuser",
        "password": "testpass"
    } 