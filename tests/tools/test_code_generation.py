import pytest
from typing import Dict, Any
from src.tools.code_generation import CodeGenerationTool
from src.tools.base import ToolResult

@pytest.fixture
def code_generation_tool():
    return CodeGenerationTool()

@pytest.fixture
def sample_form_analysis():
    return {
        "form_name": "TestForm",
        "elements": [
            {
                "name": "username",
                "type": "text",
                "required": True,
                "validation": [
                    {
                        "type": "required",
                        "message": "Username is required"
                    },
                    {
                        "type": "min_length",
                        "value": 3,
                        "message": "Username must be at least 3 characters"
                    }
                ],
                "attributes": {
                    "placeholder": "Enter username"
                }
            },
            {
                "name": "email",
                "type": "email",
                "required": True,
                "validation": [
                    {
                        "type": "required",
                        "message": "Email is required"
                    },
                    {
                        "type": "email",
                        "message": "Invalid email format"
                    }
                ],
                "attributes": {
                    "placeholder": "Enter email"
                }
            },
            {
                "name": "age",
                "type": "number",
                "required": False,
                "validation": [
                    {
                        "type": "min",
                        "value": 18,
                        "message": "Age must be at least 18"
                    },
                    {
                        "type": "max",
                        "value": 120,
                        "message": "Age must be less than 120"
                    }
                ],
                "attributes": {
                    "min": 18,
                    "max": 120
                }
            }
        ],
        "events": [
            {
                "name": "validate_age",
                "type": "validation",
                "description": "Validate age input",
                "error_message": "Invalid age value"
            },
            {
                "name": "calculate_total",
                "type": "calculation",
                "description": "Calculate total from values"
            }
        ]
    }

@pytest.mark.asyncio
async def test_code_generation_tool_initialization(code_generation_tool):
    """Test CodeGenerationTool initialization."""
    assert code_generation_tool.name == "code_generation"
    assert code_generation_tool.description == "Generates modern code from form analysis"

@pytest.mark.asyncio
async def test_code_generation_tool_validate_params(code_generation_tool):
    """Test parameter validation."""
    # Test with valid parameters
    valid_params = {"analysis": {}}
    assert await code_generation_tool.validate_params(valid_params) is True

    # Test with missing required parameter
    invalid_params = {}
    assert await code_generation_tool.validate_params(invalid_params) is False

@pytest.mark.asyncio
async def test_code_generation_tool_execute(code_generation_tool, sample_form_analysis):
    """Test code generation execution."""
    params = {
        "analysis": sample_form_analysis,
        "language": "python",
        "framework": "fastapi"
    }
    
    result = await code_generation_tool.execute(params, {})
    
    assert isinstance(result, ToolResult)
    assert result.success is True
    assert "api_code" in result.data
    assert "html_code" in result.data
    assert "validation_code" in result.data
    assert "event_code" in result.data
    
    # Verify API code structure
    api_code = result.data["api_code"]
    assert "main" in api_code
    assert "models" in api_code
    assert "routes" in api_code
    
    # Verify HTML code structure
    html_code = result.data["html_code"]
    assert "form" in html_code
    assert "styles" in html_code
    assert "scripts" in html_code
    
    # Verify validation code structure
    validation_code = result.data["validation_code"]
    assert "validators" in validation_code
    assert "error_handlers" in validation_code
    
    # Verify event code structure
    event_code = result.data["event_code"]
    assert "handlers" in event_code
    assert "utilities" in event_code

@pytest.mark.asyncio
async def test_code_generation_tool_error_handling(code_generation_tool):
    """Test error handling in code generation."""
    # Test with invalid analysis data
    invalid_params = {
        "analysis": None,
        "language": "python",
        "framework": "fastapi"
    }
    
    result = await code_generation_tool.execute(invalid_params, {})
    
    assert isinstance(result, ToolResult)
    assert result.success is False
    assert result.error is not None

@pytest.mark.asyncio
async def test_code_generation_tool_field_preparation(code_generation_tool, sample_form_analysis):
    """Test field data preparation for templates."""
    fields = code_generation_tool._prepare_fields(sample_form_analysis)
    
    assert len(fields) == 3
    
    # Verify username field
    username_field = next(f for f in fields if f["name"] == "username")
    assert username_field["type"] == "string"
    assert username_field["required"] is True
    assert len(username_field["validation"]) == 2
    assert username_field["attributes"]["placeholder"] == "Enter username"
    
    # Verify email field
    email_field = next(f for f in fields if f["name"] == "email")
    assert email_field["type"] == "string"
    assert email_field["required"] is True
    assert len(email_field["validation"]) == 2
    assert email_field["attributes"]["placeholder"] == "Enter email"
    
    # Verify age field
    age_field = next(f for f in fields if f["name"] == "age")
    assert age_field["type"] == "number"
    assert age_field["required"] is False
    assert len(age_field["validation"]) == 2
    assert age_field["attributes"]["min"] == 18
    assert age_field["attributes"]["max"] == 120

@pytest.mark.asyncio
async def test_code_generation_tool_input_type_mapping(code_generation_tool):
    """Test HTML input type to data type mapping."""
    type_mapping = {
        "text": "string",
        "number": "number",
        "email": "string",
        "password": "string",
        "date": "date",
        "datetime": "datetime",
        "checkbox": "boolean",
        "radio": "string",
        "select": "string",
        "textarea": "string",
        "unknown": "string"  # Default type
    }
    
    for html_type, data_type in type_mapping.items():
        assert code_generation_tool._map_input_type(html_type) == data_type 