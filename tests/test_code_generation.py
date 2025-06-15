import pytest
import os
import json
from src.agents.code_generation import CodeGenerationAgent

@pytest.fixture
def code_generation_agent():
    """Create a CodeGenerationAgent instance for testing."""
    agent = CodeGenerationAgent()
    agent.initialize()
    return agent

def test_initialize(code_generation_agent):
    """Test agent initialization."""
    assert code_generation_agent is not None
    assert os.path.exists("templates")
    assert os.path.exists("templates/python_api.py.j2")
    assert os.path.exists("templates/java_api.java.j2")
    assert os.path.exists("templates/csharp_api.cs.j2")
    assert os.path.exists("templates/html_form.html.j2")

def test_prepare_fields(code_generation_agent):
    """Test field preparation for code generation."""
    analyzed_data = [
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
        }
    ]
    
    prepared_fields = code_generation_agent._prepare_fields(analyzed_data)
    assert len(prepared_fields) == 2
    assert prepared_fields[0]["type"] == "string"
    assert prepared_fields[1]["type"] == "number"
    assert "validation" in prepared_fields[0]
    assert "validation" in prepared_fields[1]

def test_map_input_type(code_generation_agent):
    """Test input type mapping."""
    assert code_generation_agent._map_input_type("text") == "string"
    assert code_generation_agent._map_input_type("number") == "number"
    assert code_generation_agent._map_input_type("email") == "string"
    assert code_generation_agent._map_input_type("date") == "string"
    assert code_generation_agent._map_input_type("select") == "string"

def test_get_file_extension(code_generation_agent):
    """Test file extension determination."""
    assert code_generation_agent._get_file_extension("python") == ".py"
    assert code_generation_agent._get_file_extension("java") == ".java"
    assert code_generation_agent._get_file_extension("csharp") == ".cs"
    assert code_generation_agent._get_file_extension("html") == ".html"

def test_generate_api_code(code_generation_agent):
    """Test API code generation."""
    analyzed_data = [
        {
            "id": "field1",
            "name": "field1",
            "type": "text",
            "validation_rules": ["required"],
            "events": [],
            "is_postback": False
        }
    ]
    
    # Test Python API generation
    python_code = code_generation_agent._generate_api_code(analyzed_data, "python")
    assert "from fastapi import FastAPI" in python_code
    assert "class FormData" in python_code
    assert "field1: str" in python_code
    
    # Test Java API generation
    java_code = code_generation_agent._generate_api_code(analyzed_data, "java")
    assert "import org.springframework.web.bind.annotation" in java_code
    assert "class FormData" in java_code
    assert "private String field1" in java_code
    
    # Test C# API generation
    csharp_code = code_generation_agent._generate_api_code(analyzed_data, "csharp")
    assert "using Microsoft.AspNetCore.Mvc" in csharp_code
    assert "public class FormData" in csharp_code
    assert "public string Field1" in csharp_code

def test_generate_html_form(code_generation_agent):
    """Test HTML form generation."""
    analyzed_data = [
        {
            "id": "field1",
            "name": "field1",
            "type": "text",
            "validation_rules": ["required"],
            "events": [],
            "is_postback": False
        },
        {
            "id": "field2",
            "name": "field2",
            "type": "number",
            "validation_rules": ["min", "max"],
            "events": [],
            "is_postback": False
        }
    ]
    
    html_code = code_generation_agent._generate_html_form(analyzed_data)
    assert "<form" in html_code
    assert 'id="field1"' in html_code
    assert 'type="text"' in html_code
    assert 'required' in html_code
    assert 'id="field2"' in html_code
    assert 'type="number"' in html_code
    assert 'min=' in html_code
    assert 'max=' in html_code

def test_execute(code_generation_agent):
    """Test the main execute method."""
    analyzed_data = [
        {
            "id": "field1",
            "name": "field1",
            "type": "text",
            "validation_rules": ["required"],
            "events": [],
            "is_postback": False
        }
    ]
    
    result = code_generation_agent.execute({
        "analyzed_data": analyzed_data,
        "language": "python"
    })
    
    assert result["status"] == "success"
    assert "api_code" in result
    assert "html_code" in result
    assert "from fastapi import FastAPI" in result["api_code"]
    assert "<form" in result["html_code"]

def test_cleanup(code_generation_agent):
    """Test cleanup of resources."""
    code_generation_agent.cleanup()
    # Add assertions for cleanup if needed 