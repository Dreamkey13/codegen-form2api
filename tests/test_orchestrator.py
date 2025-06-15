import pytest
from unittest.mock import Mock, patch
from src.agents.orchestrator import OrchestratorAgent

@pytest.fixture
async def orchestrator_agent():
    """Create an OrchestratorAgent instance for testing."""
    agent = OrchestratorAgent()
    await agent.initialize()
    yield agent
    await agent.cleanup()

@pytest.mark.asyncio
async def test_initialize(orchestrator_agent):
    """Test agent initialization."""
    assert orchestrator_agent is not None
    assert "web_navigation" in orchestrator_agent.agents
    assert "form_analysis" in orchestrator_agent.agents
    assert "code_generation" in orchestrator_agent.agents

@pytest.mark.asyncio
async def test_execute_web_navigation(orchestrator_agent):
    """Test web navigation execution."""
    # Mock the web navigation agent
    mock_result = {
        "status": "success",
        "form_data": [{"id": "test", "type": "text"}]
    }
    orchestrator_agent.agents["web_navigation"].execute = Mock(return_value=mock_result)
    
    result = await orchestrator_agent._execute_web_navigation({
        "url": "https://example.com",
        "platform": "test-platform",
        "form_name": "test-form"
    })
    
    assert result["status"] == "success"
    assert "form_data" in result
    orchestrator_agent.agents["web_navigation"].execute.assert_called_once()

@pytest.mark.asyncio
async def test_execute_form_analysis(orchestrator_agent):
    """Test form analysis execution."""
    # Mock the form analysis agent
    mock_result = {
        "status": "success",
        "analyzed_data": [{"id": "test", "type": "text"}],
        "csv_data": "test,csv,data",
        "summary": {"total_elements": 1}
    }
    orchestrator_agent.agents["form_analysis"].execute = Mock(return_value=mock_result)
    
    result = await orchestrator_agent._execute_form_analysis({
        "form_data": [{"id": "test", "type": "text"}]
    })
    
    assert result["status"] == "success"
    assert "analyzed_data" in result
    assert "csv_data" in result
    assert "summary" in result
    orchestrator_agent.agents["form_analysis"].execute.assert_called_once()

@pytest.mark.asyncio
async def test_execute_code_generation(orchestrator_agent):
    """Test code generation execution."""
    # Mock the code generation agent
    mock_result = {
        "status": "success",
        "api_code": "test api code",
        "html_code": "test html code"
    }
    orchestrator_agent.agents["code_generation"].execute = Mock(return_value=mock_result)
    
    result = await orchestrator_agent._execute_code_generation({
        "analyzed_data": [{"id": "test", "type": "text"}],
        "language": "python"
    })
    
    assert result["status"] == "success"
    assert "api_code" in result
    assert "html_code" in result
    orchestrator_agent.agents["code_generation"].execute.assert_called_once()

@pytest.mark.asyncio
async def test_prepare_output_package(orchestrator_agent):
    """Test output package preparation."""
    web_nav_result = {
        "status": "success",
        "form_data": [{"id": "test", "type": "text"}]
    }
    form_analysis_result = {
        "status": "success",
        "analyzed_data": [{"id": "test", "type": "text"}],
        "csv_data": "test,csv,data",
        "summary": {"total_elements": 1}
    }
    code_gen_result = {
        "status": "success",
        "api_code": "test api code",
        "html_code": "test html code"
    }
    
    output = orchestrator_agent._prepare_output_package(
        web_nav_result,
        form_analysis_result,
        code_gen_result
    )
    
    assert output["status"] == "success"
    assert "form_data" in output
    assert "analyzed_data" in output
    assert "csv_data" in output
    assert "summary" in output
    assert "api_code" in output
    assert "html_code" in output

@pytest.mark.asyncio
async def test_execute_full_workflow(orchestrator_agent):
    """Test the complete workflow execution."""
    # Mock all agents
    web_nav_mock = Mock(return_value={
        "status": "success",
        "form_data": [{"id": "test", "type": "text"}]
    })
    form_analysis_mock = Mock(return_value={
        "status": "success",
        "analyzed_data": [{"id": "test", "type": "text"}],
        "csv_data": "test,csv,data",
        "summary": {"total_elements": 1}
    })
    code_gen_mock = Mock(return_value={
        "status": "success",
        "api_code": "test api code",
        "html_code": "test html code"
    })
    
    orchestrator_agent.agents["web_navigation"].execute = web_nav_mock
    orchestrator_agent.agents["form_analysis"].execute = form_analysis_mock
    orchestrator_agent.agents["code_generation"].execute = code_gen_mock
    
    result = await orchestrator_agent.execute({
        "url": "https://example.com",
        "platform": "test-platform",
        "form_name": "test-form",
        "language": "python"
    })
    
    assert result["status"] == "success"
    assert "form_data" in result
    assert "analyzed_data" in result
    assert "csv_data" in result
    assert "summary" in result
    assert "api_code" in result
    assert "html_code" in result
    
    web_nav_mock.assert_called_once()
    form_analysis_mock.assert_called_once()
    code_gen_mock.assert_called_once()

@pytest.mark.asyncio
async def test_error_handling(orchestrator_agent):
    """Test error handling in the workflow."""
    # Mock web navigation to fail
    orchestrator_agent.agents["web_navigation"].execute = Mock(return_value={
        "status": "error",
        "error": "Navigation failed"
    })
    
    result = await orchestrator_agent.execute({
        "url": "https://example.com",
        "platform": "test-platform",
        "form_name": "test-form",
        "language": "python"
    })
    
    assert result["status"] == "error"
    assert "error" in result
    assert result["error"] == "Navigation failed"
    
    # Mock form analysis to fail
    orchestrator_agent.agents["web_navigation"].execute = Mock(return_value={
        "status": "success",
        "form_data": [{"id": "test", "type": "text"}]
    })
    orchestrator_agent.agents["form_analysis"].execute = Mock(return_value={
        "status": "error",
        "error": "Analysis failed"
    })
    
    result = await orchestrator_agent.execute({
        "url": "https://example.com",
        "platform": "test-platform",
        "form_name": "test-form",
        "language": "python"
    })
    
    assert result["status"] == "error"
    assert "error" in result
    assert result["error"] == "Analysis failed"
    
    # Mock code generation to fail
    orchestrator_agent.agents["form_analysis"].execute = Mock(return_value={
        "status": "success",
        "analyzed_data": [{"id": "test", "type": "text"}],
        "csv_data": "test,csv,data",
        "summary": {"total_elements": 1}
    })
    orchestrator_agent.agents["code_generation"].execute = Mock(return_value={
        "status": "error",
        "error": "Code generation failed"
    })
    
    result = await orchestrator_agent.execute({
        "url": "https://example.com",
        "platform": "test-platform",
        "form_name": "test-form",
        "language": "python"
    })
    
    assert result["status"] == "error"
    assert "error" in result
    assert result["error"] == "Code generation failed" 