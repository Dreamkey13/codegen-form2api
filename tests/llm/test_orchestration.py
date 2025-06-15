import pytest
from unittest.mock import Mock, AsyncMock
from src.llm.orchestration import (
    OrchestrationStep,
    OrchestrationPlan,
    BaseOrchestrator,
    FormMigrationOrchestrator
)
from src.llm.base import LLMResponse
from src.tools.base import ToolResult

@pytest.fixture
def mock_llm():
    llm = Mock()
    llm.generate_response = AsyncMock(return_value=LLMResponse(
        success=True,
        data="Test response",
        error=None
    ))
    return llm

@pytest.fixture
def mock_tool():
    tool = Mock()
    tool.execute = AsyncMock(return_value=ToolResult(
        success=True,
        data="Test result",
        error=None,
        metadata={}
    ))
    return tool

@pytest.fixture
def mock_tool_registry(mock_tool):
    registry = Mock()
    registry.get_tool = Mock(return_value=mock_tool)
    return registry

@pytest.fixture
def orchestrator(mock_llm, mock_tool_registry):
    return FormMigrationOrchestrator(
        llm=mock_llm,
        tool_registry=mock_tool_registry
    )

def test_orchestration_step_creation():
    step = OrchestrationStep(
        name="test_step",
        description="Test step description",
        tool_name="test_tool",
        tool_params={"param1": "value1"},
        llm_prompt="Test prompt",
        required=True
    )
    
    assert step.name == "test_step"
    assert step.description == "Test step description"
    assert step.tool_name == "test_tool"
    assert step.tool_params == {"param1": "value1"}
    assert step.llm_prompt == "Test prompt"
    assert step.required is True
    assert step.result is None
    assert step.error is None

def test_orchestration_plan_creation():
    steps = [
        OrchestrationStep("step1", "Step 1"),
        OrchestrationStep("step2", "Step 2")
    ]
    plan = OrchestrationPlan(steps)
    
    assert len(plan.steps) == 2
    assert plan.current_step_index == 0
    assert plan.results == {}
    assert plan.errors == {}

def test_orchestration_plan_step_management():
    steps = [
        OrchestrationStep("step1", "Step 1"),
        OrchestrationStep("step2", "Step 2")
    ]
    plan = OrchestrationPlan(steps)
    
    # Test getting next step
    step1 = plan.get_next_step()
    assert step1.name == "step1"
    assert plan.current_step_index == 1
    
    step2 = plan.get_next_step()
    assert step2.name == "step2"
    assert plan.current_step_index == 2
    
    # Test completion
    assert plan.is_complete() is True
    assert plan.get_next_step() is None

def test_orchestration_plan_results():
    plan = OrchestrationPlan([OrchestrationStep("step1", "Step 1")])
    
    # Test adding results
    plan.add_result("step1", "test result")
    assert plan.results["step1"] == "test result"
    
    # Test adding errors
    plan.add_error("step1", "test error")
    assert plan.errors["step1"] == "test error"

@pytest.mark.asyncio
async def test_form_migration_orchestrator_plan_creation(orchestrator):
    context = {"form_url": "http://example.com/form"}
    plan = await orchestrator.create_plan(context)
    
    assert len(plan.steps) == 5
    assert plan.steps[0].name == "analyze_form"
    assert plan.steps[0].tool_name == "web_navigation"
    assert plan.steps[0].tool_params["url"] == "http://example.com/form"

@pytest.mark.asyncio
async def test_orchestrator_execute_tool_step(orchestrator, mock_tool):
    step = OrchestrationStep(
        name="test_step",
        description="Test step",
        tool_name="test_tool",
        tool_params={"param1": "value1"}
    )
    
    result = await orchestrator._execute_tool_step(step)
    assert result == "Test result"
    mock_tool.execute.assert_called_once_with({"param1": "value1"})

@pytest.mark.asyncio
async def test_orchestrator_execute_llm_step(orchestrator, mock_llm):
    step = OrchestrationStep(
        name="test_step",
        description="Test step",
        llm_prompt="Test prompt"
    )
    
    result = await orchestrator._execute_llm_step(step)
    assert result == "Test response"
    mock_llm.generate_response.assert_called_once_with("Test prompt")

@pytest.mark.asyncio
async def test_orchestrator_execute_plan(orchestrator):
    steps = [
        OrchestrationStep(
            name="step1",
            description="Step 1",
            tool_name="test_tool",
            tool_params={"param1": "value1"}
        ),
        OrchestrationStep(
            name="step2",
            description="Step 2",
            llm_prompt="Test prompt"
        )
    ]
    plan = OrchestrationPlan(steps)
    
    results = await orchestrator.execute_plan(plan)
    
    assert results["success"] is True
    assert "step1" in results["results"]
    assert "step2" in results["results"]
    assert len(results["errors"]) == 0

@pytest.mark.asyncio
async def test_orchestrator_execute_plan_with_error(orchestrator, mock_tool):
    mock_tool.execute.side_effect = Exception("Test error")
    
    steps = [
        OrchestrationStep(
            name="step1",
            description="Step 1",
            tool_name="test_tool",
            tool_params={"param1": "value1"},
            required=True
        ),
        OrchestrationStep(
            name="step2",
            description="Step 2",
            llm_prompt="Test prompt"
        )
    ]
    plan = OrchestrationPlan(steps)
    
    results = await orchestrator.execute_plan(plan)
    
    assert results["success"] is False
    assert "step1" in results["errors"]
    assert "step2" not in results["results"]

@pytest.mark.asyncio
async def test_form_migration_orchestrator_context_passing(orchestrator):
    context = {"form_url": "http://example.com/form"}
    plan = await orchestrator.create_plan(context)
    
    # Mock the results of the first step
    plan.add_result("analyze_form", {"form_data": "test data"})
    
    # Execute the plan
    results = await orchestrator.execute_plan(plan)
    
    # Verify that the context was passed correctly
    assert results["success"] is True
    assert "analyze_form" in results["results"]
    assert "validate_analysis" in results["results"]
    assert "generate_api" in results["results"]
    assert "generate_form" in results["results"]
    assert "validate_output" in results["results"] 