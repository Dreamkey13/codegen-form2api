import pytest
import json
from src.agents.form_analysis import FormAnalysisAgent

@pytest.fixture
def form_analysis_agent():
    """Create a FormAnalysisAgent instance for testing."""
    agent = FormAnalysisAgent()
    agent.initialize()
    return agent

def test_initialize(form_analysis_agent):
    """Test agent initialization."""
    assert form_analysis_agent is not None

def test_analyze_elements(form_analysis_agent):
    """Test form element analysis."""
    form_data = [
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
        }
    ]
    
    analyzed_data = form_analysis_agent._analyze_elements(form_data)
    assert len(analyzed_data) == 2
    assert analyzed_data[0]["validation_rules"] == ["required", "pattern"]
    assert analyzed_data[1]["validation_rules"] == ["min", "max"]

def test_generate_selector(form_analysis_agent):
    """Test selector generation."""
    element = {
        "id": "test-field",
        "name": "test-field",
        "type": "text"
    }
    
    selector = form_analysis_agent._generate_selector(element)
    assert selector == "#test-field"

def test_detect_events(form_analysis_agent):
    """Test event detection."""
    element = {
        "id": "test-field",
        "name": "test-field",
        "type": "text",
        "onchange": "handleChange()",
        "onblur": "validateField()"
    }
    
    events = form_analysis_agent._detect_events(element)
    assert "onchange" in events
    assert "onblur" in events
    assert len(events) == 2

def test_detect_postback_triggers(form_analysis_agent):
    """Test postback trigger detection."""
    element = {
        "id": "submit-button",
        "name": "submit-button",
        "type": "submit",
        "onclick": "__doPostBack('submit-button', '')"
    }
    
    is_postback = form_analysis_agent._detect_postback_triggers(element)
    assert is_postback is True

def test_generate_csv(form_analysis_agent):
    """Test CSV generation."""
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
    
    csv_data = form_analysis_agent._generate_csv(analyzed_data)
    assert "field1,text,required;pattern,onchange,False" in csv_data
    assert "field2,number,min;max,,False" in csv_data

def test_generate_summary(form_analysis_agent):
    """Test summary generation."""
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
    
    summary = form_analysis_agent._generate_summary(analyzed_data)
    assert summary["total_elements"] == 2
    assert summary["input_types"]["text"] == 1
    assert summary["input_types"]["number"] == 1
    assert summary["required_fields"] == 1
    assert summary["postback_triggers"] == 0

def test_count_input_types(form_analysis_agent):
    """Test input type counting."""
    analyzed_data = [
        {"type": "text"},
        {"type": "number"},
        {"type": "text"},
        {"type": "select"}
    ]
    
    type_counts = form_analysis_agent._count_input_types(analyzed_data)
    assert type_counts["text"] == 2
    assert type_counts["number"] == 1
    assert type_counts["select"] == 1

def test_execute(form_analysis_agent):
    """Test the main execute method."""
    form_data = [
        {
            "id": "field1",
            "name": "field1",
            "type": "text",
            "required": "true"
        }
    ]
    
    result = form_analysis_agent.execute({
        "form_data": form_data
    })
    
    assert result["status"] == "success"
    assert "analyzed_data" in result
    assert "csv_data" in result
    assert "summary" in result
    assert len(result["analyzed_data"]) == 1 