import pytest
import asyncio
from unittest.mock import Mock, patch
from src.agents.web_navigation import WebNavigationAgent

@pytest.fixture
async def web_navigation_agent():
    """Create a WebNavigationAgent instance for testing."""
    agent = WebNavigationAgent()
    await agent.initialize()
    yield agent
    await agent.cleanup()

@pytest.mark.asyncio
async def test_initialize(web_navigation_agent):
    """Test agent initialization."""
    assert web_navigation_agent.browser is not None
    assert web_navigation_agent.context is not None
    assert web_navigation_agent.page is not None

@pytest.mark.asyncio
async def test_navigate_to_url(web_navigation_agent):
    """Test URL navigation."""
    url = "https://example.com"
    await web_navigation_agent._navigate_to_url(url)
    current_url = web_navigation_agent.page.url
    assert current_url.startswith(url)

@pytest.mark.asyncio
async def test_select_platform(web_navigation_agent):
    """Test platform selection."""
    # Mock the page content
    web_navigation_agent.page.content = Mock(return_value="<select id='platform'><option value='platform1'>Platform 1</option></select>")
    
    # Mock the select method
    web_navigation_agent.page.select_option = Mock()
    
    await web_navigation_agent._select_platform("platform1")
    web_navigation_agent.page.select_option.assert_called_once()

@pytest.mark.asyncio
async def test_select_form(web_navigation_agent):
    """Test form selection."""
    # Mock the page content
    web_navigation_agent.page.content = Mock(return_value="<select id='form'><option value='form1'>Form 1</option></select>")
    
    # Mock the select method
    web_navigation_agent.page.select_option = Mock()
    
    await web_navigation_agent._select_form("form1")
    web_navigation_agent.page.select_option.assert_called_once()

@pytest.mark.asyncio
async def test_click_button(web_navigation_agent):
    """Test button clicking."""
    # Mock the page content
    web_navigation_agent.page.content = Mock(return_value="<button id='test-button'>Click Me</button>")
    
    # Mock the click method
    web_navigation_agent.page.click = Mock()
    
    await web_navigation_agent._click_button("test-button")
    web_navigation_agent.page.click.assert_called_once_with("#test-button")

@pytest.mark.asyncio
async def test_handle_user_identification(web_navigation_agent):
    """Test user identification handling."""
    # Mock the page content
    web_navigation_agent.page.content = Mock(return_value="<input id='username'><input id='password'>")
    
    # Mock the fill method
    web_navigation_agent.page.fill = Mock()
    
    await web_navigation_agent._handle_user_identification("testuser", "testpass")
    assert web_navigation_agent.page.fill.call_count == 2

@pytest.mark.asyncio
async def test_get_form_data(web_navigation_agent):
    """Test form data retrieval."""
    # Mock the page content
    web_navigation_agent.page.content = Mock(return_value="""
        <form>
            <input type="text" id="field1" name="field1">
            <input type="number" id="field2" name="field2">
            <select id="field3" name="field3">
                <option value="1">Option 1</option>
            </select>
        </form>
    """)
    
    # Mock the query_selector_all method
    web_navigation_agent.page.query_selector_all = Mock(return_value=[
        Mock(get_attribute=Mock(side_effect=lambda attr: {
            "id": "field1",
            "name": "field1",
            "type": "text"
        }.get(attr))),
        Mock(get_attribute=Mock(side_effect=lambda attr: {
            "id": "field2",
            "name": "field2",
            "type": "number"
        }.get(attr))),
        Mock(get_attribute=Mock(side_effect=lambda attr: {
            "id": "field3",
            "name": "field3",
            "type": "select-one"
        }.get(attr)))
    ])
    
    form_data = await web_navigation_agent._get_form_data()
    assert len(form_data) == 3
    assert form_data[0]["id"] == "field1"
    assert form_data[1]["type"] == "number"
    assert form_data[2]["name"] == "field3"

@pytest.mark.asyncio
async def test_get_element_info(web_navigation_agent):
    """Test element information retrieval."""
    # Mock element
    element = Mock(
        get_attribute=Mock(side_effect=lambda attr: {
            "id": "test-element",
            "name": "test-element",
            "type": "text",
            "required": "true",
            "pattern": "[A-Za-z]+",
            "min": "0",
            "max": "100"
        }.get(attr))
    )
    
    info = await web_navigation_agent._get_element_info(element)
    assert info["id"] == "test-element"
    assert info["type"] == "text"
    assert info["required"] == "true"
    assert info["pattern"] == "[A-Za-z]+"
    assert info["min"] == "0"
    assert info["max"] == "100"

@pytest.mark.asyncio
async def test_execute(web_navigation_agent):
    """Test the main execute method."""
    # Mock all the necessary methods
    web_navigation_agent._navigate_to_url = Mock()
    web_navigation_agent._select_platform = Mock()
    web_navigation_agent._select_form = Mock()
    web_navigation_agent._click_button = Mock()
    web_navigation_agent._handle_user_identification = Mock()
    web_navigation_agent._get_form_data = Mock(return_value=[{"id": "test", "type": "text"}])
    
    result = await web_navigation_agent.execute({
        "url": "https://example.com",
        "platform": "test-platform",
        "form_name": "test-form",
        "username": "testuser",
        "password": "testpass"
    })
    
    assert result["status"] == "success"
    assert "form_data" in result
    assert len(result["form_data"]) == 1 