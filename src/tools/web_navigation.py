from typing import Dict, Any, List, Optional
import asyncio
from playwright.async_api import async_playwright, Browser, Page
from .base import BaseTool, ToolConfig, ToolResult

class WebNavigationTool(BaseTool):
    """Tool for web navigation and form element extraction."""

    def __init__(self):
        super().__init__(
            ToolConfig(
                name="web_navigation",
                description="Handles web form navigation and element extraction"
            )
        )
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        """Execute web navigation and form extraction."""
        try:
            url = params["url"]
            await self._initialize_browser()
            await self._navigate_to_url(url)
            
            # Extract form elements
            elements = await self._extract_form_elements()
            
            # Extract validation rules
            validation_rules = await self._extract_validation_rules()
            
            # Extract event handlers
            event_handlers = await self._extract_event_handlers()
            
            return ToolResult(
                success=True,
                data={
                    "elements": elements,
                    "validation_rules": validation_rules,
                    "event_handlers": event_handlers
                },
                metadata={
                    "url": url,
                    "timestamp": asyncio.get_event_loop().time()
                }
            )
        except Exception as e:
            self.logger.error(f"Error in web navigation: {str(e)}")
            return ToolResult(
                success=False,
                data={},
                error=str(e)
            )
        finally:
            await self.cleanup()

    async def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate the input parameters."""
        required_params = ["url"]
        return all(param in params for param in required_params)

    async def cleanup(self):
        """Clean up browser resources."""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()

    async def _initialize_browser(self):
        """Initialize the browser instance."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )
        self.page = await self.browser.new_page()

    async def _navigate_to_url(self, url: str):
        """Navigate to the specified URL."""
        await self.page.goto(url, wait_until="networkidle")
        await self.page.wait_for_load_state("domcontentloaded")

    async def _extract_form_elements(self) -> List[Dict[str, Any]]:
        """Extract form elements and their properties."""
        elements = await self.page.query_selector_all("form input, form select, form textarea")
        form_data = []
        
        for element in elements:
            element_data = await self._get_element_properties(element)
            form_data.append(element_data)
        
        return form_data

    async def _get_element_properties(self, element) -> Dict[str, Any]:
        """Get properties of a form element."""
        return {
            "id": await element.get_attribute("id"),
            "name": await element.get_attribute("name"),
            "type": await element.get_attribute("type"),
            "required": await element.get_attribute("required") is not None,
            "value": await element.get_attribute("value"),
            "placeholder": await element.get_attribute("placeholder"),
            "class": await element.get_attribute("class"),
            "disabled": await element.get_attribute("disabled") is not None,
            "readonly": await element.get_attribute("readonly") is not None,
            "maxlength": await element.get_attribute("maxlength"),
            "min": await element.get_attribute("min"),
            "max": await element.get_attribute("max"),
            "pattern": await element.get_attribute("pattern")
        }

    async def _extract_validation_rules(self) -> Dict[str, Any]:
        """Extract form validation rules."""
        validation_rules = {}
        
        # Extract client-side validation rules
        validation_script = """
        () => {
            const rules = {};
            document.querySelectorAll('form').forEach(form => {
                const formRules = {};
                form.querySelectorAll('input, select, textarea').forEach(element => {
                    formRules[element.name || element.id] = {
                        required: element.required,
                        pattern: element.pattern,
                        min: element.min,
                        max: element.max,
                        minLength: element.minLength,
                        maxLength: element.maxLength
                    };
                });
                rules[form.id || 'default'] = formRules;
            });
            return rules;
        }
        """
        
        validation_rules["client_side"] = await self.page.evaluate(validation_script)
        
        # Extract server-side validation rules (if available)
        # This would require additional analysis of the server-side code
        validation_rules["server_side"] = {}
        
        return validation_rules

    async def _extract_event_handlers(self) -> Dict[str, Any]:
        """Extract form event handlers."""
        event_handlers = {}
        
        # Extract client-side event handlers
        event_script = """
        () => {
            const handlers = {};
            document.querySelectorAll('form').forEach(form => {
                const formHandlers = {};
                form.querySelectorAll('*').forEach(element => {
                    const elementHandlers = {};
                    for (const prop in element) {
                        if (prop.startsWith('on') && typeof element[prop] === 'function') {
                            elementHandlers[prop] = true;
                        }
                    }
                    if (Object.keys(elementHandlers).length > 0) {
                        formHandlers[element.id || element.name] = elementHandlers;
                    }
                });
                handlers[form.id || 'default'] = formHandlers;
            });
            return handlers;
        }
        """
        
        event_handlers["client_side"] = await self.page.evaluate(event_script)
        
        # Extract server-side event handlers (if available)
        # This would require additional analysis of the server-side code
        event_handlers["server_side"] = {}
        
        return event_handlers 