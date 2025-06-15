import pytest
from typing import Dict, Any
from src.tools.web_navigation import WebNavigationTool
from src.tools.base import ToolResult
from playwright.async_api import async_playwright

@pytest.fixture
def web_navigation_tool():
    return WebNavigationTool()

@pytest.fixture
async def mock_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        yield page
        await browser.close()

@pytest.mark.asyncio
async def test_web_navigation_tool_initialization(web_navigation_tool):
    """Test WebNavigationTool initialization."""
    assert web_navigation_tool.name == "web_navigation"
    assert web_navigation_tool.description == "Navigates web forms and extracts elements"

@pytest.mark.asyncio
async def test_web_navigation_tool_validate_params(web_navigation_tool):
    """Test parameter validation."""
    # Test with valid parameters
    valid_params = {"url": "http://example.com"}
    assert await web_navigation_tool.validate_params(valid_params) is True

    # Test with missing required parameter
    invalid_params = {}
    assert await web_navigation_tool.validate_params(invalid_params) is False

@pytest.mark.asyncio
async def test_web_navigation_tool_execute(web_navigation_tool, mock_page):
    """Test web navigation execution."""
    # Mock page content
    await mock_page.set_content("""
        <form id="testForm">
            <input type="text" name="username" required placeholder="Enter username">
            <input type="email" name="email" required placeholder="Enter email">
            <input type="number" name="age" min="18" max="120">
            <select name="country">
                <option value="us">United States</option>
                <option value="ca">Canada</option>
            </select>
            <textarea name="comments"></textarea>
        </form>
    """)
    
    web_navigation_tool.page = mock_page
    
    params = {
        "url": "http://example.com",
        "wait_for": "#testForm"
    }
    
    result = await web_navigation_tool.execute(params, {})
    
    assert isinstance(result, ToolResult)
    assert result.success is True
    assert "elements" in result.data
    assert "validation_rules" in result.data
    assert "event_handlers" in result.data
    
    # Verify extracted elements
    elements = result.data["elements"]
    assert len(elements) == 5
    
    # Verify username input
    username_input = next(e for e in elements if e["name"] == "username")
    assert username_input["type"] == "text"
    assert username_input["required"] is True
    assert username_input["attributes"]["placeholder"] == "Enter username"
    
    # Verify email input
    email_input = next(e for e in elements if e["name"] == "email")
    assert email_input["type"] == "email"
    assert email_input["required"] is True
    assert email_input["attributes"]["placeholder"] == "Enter email"
    
    # Verify age input
    age_input = next(e for e in elements if e["name"] == "age")
    assert age_input["type"] == "number"
    assert age_input["required"] is False
    assert age_input["attributes"]["min"] == "18"
    assert age_input["attributes"]["max"] == "120"
    
    # Verify select element
    country_select = next(e for e in elements if e["name"] == "country")
    assert country_select["type"] == "select"
    assert len(country_select["options"]) == 2
    assert country_select["options"][0]["value"] == "us"
    assert country_select["options"][0]["label"] == "United States"
    
    # Verify textarea
    comments_textarea = next(e for e in elements if e["name"] == "comments")
    assert comments_textarea["type"] == "textarea"

@pytest.mark.asyncio
async def test_web_navigation_tool_error_handling(web_navigation_tool):
    """Test error handling in web navigation."""
    # Test with invalid URL
    invalid_params = {
        "url": "invalid-url"
    }
    
    result = await web_navigation_tool.execute(invalid_params, {})
    
    assert isinstance(result, ToolResult)
    assert result.success is False
    assert result.error is not None

@pytest.mark.asyncio
async def test_web_navigation_tool_form_element_extraction(web_navigation_tool, mock_page):
    """Test form element extraction."""
    # Mock page with complex form
    await mock_page.set_content("""
        <form id="complexForm">
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" id="name" name="name" required 
                       pattern="[A-Za-z ]+" title="Only letters and spaces allowed">
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="phone">Phone</label>
                <input type="tel" id="phone" name="phone" 
                       pattern="[0-9]{10}" title="10-digit phone number">
            </div>
            <div class="form-group">
                <label for="dob">Date of Birth</label>
                <input type="date" id="dob" name="dob" required>
            </div>
            <div class="form-group">
                <label for="gender">Gender</label>
                <select id="gender" name="gender" required>
                    <option value="">Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="form-group">
                <label for="interests">Interests</label>
                <div>
                    <input type="checkbox" id="sports" name="interests" value="sports">
                    <label for="sports">Sports</label>
                </div>
                <div>
                    <input type="checkbox" id="music" name="interests" value="music">
                    <label for="music">Music</label>
                </div>
                <div>
                    <input type="checkbox" id="reading" name="interests" value="reading">
                    <label for="reading">Reading</label>
                </div>
            </div>
            <div class="form-group">
                <label for="comments">Comments</label>
                <textarea id="comments" name="comments" rows="4"></textarea>
            </div>
        </form>
    """)
    
    web_navigation_tool.page = mock_page
    
    elements = await web_navigation_tool._extract_form_elements()
    
    assert len(elements) == 8  # 5 inputs + 1 select + 1 textarea + 1 checkbox group
    
    # Verify name input
    name_input = next(e for e in elements if e["name"] == "name")
    assert name_input["type"] == "text"
    assert name_input["required"] is True
    assert name_input["attributes"]["pattern"] == "[A-Za-z ]+"
    assert name_input["attributes"]["title"] == "Only letters and spaces allowed"
    
    # Verify email input
    email_input = next(e for e in elements if e["name"] == "email")
    assert email_input["type"] == "email"
    assert email_input["required"] is True
    
    # Verify phone input
    phone_input = next(e for e in elements if e["name"] == "phone")
    assert phone_input["type"] == "tel"
    assert phone_input["attributes"]["pattern"] == "[0-9]{10}"
    assert phone_input["attributes"]["title"] == "10-digit phone number"
    
    # Verify date input
    dob_input = next(e for e in elements if e["name"] == "dob")
    assert dob_input["type"] == "date"
    assert dob_input["required"] is True
    
    # Verify select element
    gender_select = next(e for e in elements if e["name"] == "gender")
    assert gender_select["type"] == "select"
    assert gender_select["required"] is True
    assert len(gender_select["options"]) == 4  # Including empty option
    
    # Verify checkbox group
    interests_checkboxes = [e for e in elements if e["name"] == "interests"]
    assert len(interests_checkboxes) == 3
    assert all(c["type"] == "checkbox" for c in interests_checkboxes)
    assert {c["value"] for c in interests_checkboxes} == {"sports", "music", "reading"}
    
    # Verify textarea
    comments_textarea = next(e for e in elements if e["name"] == "comments")
    assert comments_textarea["type"] == "textarea"
    assert comments_textarea["attributes"]["rows"] == "4"

@pytest.mark.asyncio
async def test_web_navigation_tool_validation_rules_extraction(web_navigation_tool, mock_page):
    """Test validation rules extraction."""
    # Mock page with validation rules
    await mock_page.set_content("""
        <form id="validationForm">
            <input type="text" name="username" required minlength="3" maxlength="20">
            <input type="email" name="email" required>
            <input type="number" name="age" min="18" max="120">
            <input type="password" name="password" required pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$">
        </form>
    """)
    
    web_navigation_tool.page = mock_page
    
    validation_rules = await web_navigation_tool._extract_validation_rules()
    
    assert len(validation_rules) == 4
    
    # Verify username validation
    username_rules = validation_rules["username"]
    assert len(username_rules) == 3
    assert any(r["type"] == "required" for r in username_rules)
    assert any(r["type"] == "minlength" and r["value"] == 3 for r in username_rules)
    assert any(r["type"] == "maxlength" and r["value"] == 20 for r in username_rules)
    
    # Verify email validation
    email_rules = validation_rules["email"]
    assert len(email_rules) == 1
    assert any(r["type"] == "required" for r in email_rules)
    
    # Verify age validation
    age_rules = validation_rules["age"]
    assert len(age_rules) == 2
    assert any(r["type"] == "min" and r["value"] == 18 for r in age_rules)
    assert any(r["type"] == "max" and r["value"] == 120 for r in age_rules)
    
    # Verify password validation
    password_rules = validation_rules["password"]
    assert len(password_rules) == 2
    assert any(r["type"] == "required" for r in password_rules)
    assert any(r["type"] == "pattern" for r in password_rules)

@pytest.mark.asyncio
async def test_web_navigation_tool_event_handlers_extraction(web_navigation_tool, mock_page):
    """Test event handlers extraction."""
    # Mock page with event handlers
    await mock_page.set_content("""
        <form id="eventForm">
            <input type="text" name="username" onchange="validateUsername(this)">
            <input type="email" name="email" onblur="validateEmail(this)">
            <input type="number" name="age" oninput="validateAge(this)">
            <select name="country" onchange="updateCities(this)">
                <option value="us">United States</option>
                <option value="ca">Canada</option>
            </select>
        </form>
        <script>
            function validateUsername(input) {
                // Username validation logic
            }
            function validateEmail(input) {
                // Email validation logic
            }
            function validateAge(input) {
                // Age validation logic
            }
            function updateCities(select) {
                // Update cities based on country
            }
        </script>
    """)
    
    web_navigation_tool.page = mock_page
    
    event_handlers = await web_navigation_tool._extract_event_handlers()
    
    assert len(event_handlers) == 4
    
    # Verify username event handlers
    username_events = event_handlers["username"]
    assert len(username_events) == 1
    assert username_events[0]["type"] == "change"
    assert username_events[0]["handler"] == "validateUsername"
    
    # Verify email event handlers
    email_events = event_handlers["email"]
    assert len(email_events) == 1
    assert email_events[0]["type"] == "blur"
    assert email_events[0]["handler"] == "validateEmail"
    
    # Verify age event handlers
    age_events = event_handlers["age"]
    assert len(age_events) == 1
    assert age_events[0]["type"] == "input"
    assert age_events[0]["handler"] == "validateAge"
    
    # Verify country event handlers
    country_events = event_handlers["country"]
    assert len(country_events) == 1
    assert country_events[0]["type"] == "change"
    assert country_events[0]["handler"] == "updateCities" 