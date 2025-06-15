from typing import Dict, Any, List, Optional
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from .base import BaseTool, ToolConfig, ToolResult

class CodeGenerationTool(BaseTool):
    """Tool for generating modern code from form analysis."""

    def __init__(self):
        super().__init__(
            ToolConfig(
                name="code_generation",
                description="Generates modern code from form analysis"
            )
        )
        self.template_env = Environment(
            loader=FileSystemLoader("templates")
        )

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        """Execute code generation."""
        try:
            analysis = params["analysis"]
            language = params.get("language", "python")
            framework = params.get("framework", "fastapi")
            
            # Generate API code
            api_code = await self._generate_api_code(analysis, language, framework)
            
            # Generate HTML form
            html_code = await self._generate_html_form(analysis)
            
            # Generate validation code
            validation_code = await self._generate_validation_code(analysis, language)
            
            # Generate event handlers
            event_code = await self._generate_event_handlers(analysis, language)
            
            return ToolResult(
                success=True,
                data={
                    "api_code": api_code,
                    "html_code": html_code,
                    "validation_code": validation_code,
                    "event_code": event_code
                },
                metadata={
                    "language": language,
                    "framework": framework,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            self.logger.error(f"Error in code generation: {str(e)}")
            return ToolResult(
                success=False,
                data={},
                error=str(e)
            )

    async def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate the input parameters."""
        required_params = ["analysis"]
        return all(param in params for param in required_params)

    async def cleanup(self):
        """Clean up any resources."""
        pass

    async def _generate_api_code(self, analysis: Dict[str, Any], language: str, framework: str) -> Dict[str, str]:
        """Generate API code based on the analysis."""
        template_name = f"api_{language}_{framework}.jinja2"
        template = self.template_env.get_template(template_name)
        
        # Prepare template data
        template_data = {
            "form_name": analysis.get("form_name", "Form"),
            "fields": self._prepare_fields(analysis),
            "validation_rules": analysis.get("validation", {}),
            "event_handlers": analysis.get("events", {})
        }
        
        # Generate code
        code = template.render(**template_data)
        
        return {
            "main": code,
            "models": self._generate_models(analysis, language),
            "routes": self._generate_routes(analysis, language, framework)
        }

    async def _generate_html_form(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate HTML form code."""
        template = self.template_env.get_template("html_form.jinja2")
        
        # Prepare template data
        template_data = {
            "form_name": analysis.get("form_name", "Form"),
            "fields": self._prepare_fields(analysis),
            "validation_rules": analysis.get("validation", {}),
            "event_handlers": analysis.get("events", {})
        }
        
        # Generate code
        code = template.render(**template_data)
        
        return {
            "form": code,
            "styles": self._generate_styles(analysis),
            "scripts": self._generate_scripts(analysis)
        }

    async def _generate_validation_code(self, analysis: Dict[str, Any], language: str) -> Dict[str, str]:
        """Generate validation code."""
        template = self.template_env.get_template(f"validation_{language}.jinja2")
        
        # Prepare template data
        template_data = {
            "validation_rules": analysis.get("validation", {}),
            "fields": self._prepare_fields(analysis)
        }
        
        # Generate code
        code = template.render(**template_data)
        
        return {
            "validators": code,
            "error_handlers": self._generate_error_handlers(analysis, language)
        }

    async def _generate_event_handlers(self, analysis: Dict[str, Any], language: str) -> Dict[str, str]:
        """Generate event handler code."""
        template = self.template_env.get_template(f"events_{language}.jinja2")
        
        # Prepare template data
        template_data = {
            "event_handlers": analysis.get("events", {}),
            "fields": self._prepare_fields(analysis)
        }
        
        # Generate code
        code = template.render(**template_data)
        
        return {
            "handlers": code,
            "utilities": self._generate_event_utilities(analysis, language)
        }

    def _prepare_fields(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepare field data for templates."""
        fields = []
        for element in analysis.get("elements", []):
            field = {
                "name": element.get("name"),
                "type": self._map_input_type(element.get("type")),
                "required": element.get("required", False),
                "validation": element.get("validation", {}),
                "events": element.get("events", {}),
                "attributes": {
                    "placeholder": element.get("placeholder"),
                    "min": element.get("min"),
                    "max": element.get("max"),
                    "pattern": element.get("pattern")
                }
            }
            fields.append(field)
        return fields

    def _map_input_type(self, input_type: str) -> str:
        """Map HTML input types to appropriate data types."""
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
            "textarea": "string"
        }
        return type_mapping.get(input_type, "string")

    def _generate_models(self, analysis: Dict[str, Any], language: str) -> str:
        """Generate data models."""
        template = self.template_env.get_template(f"models_{language}.jinja2")
        return template.render(fields=self._prepare_fields(analysis))

    def _generate_routes(self, analysis: Dict[str, Any], language: str, framework: str) -> str:
        """Generate API routes."""
        template = self.template_env.get_template(f"routes_{language}_{framework}.jinja2")
        return template.render(
            form_name=analysis.get("form_name", "Form"),
            fields=self._prepare_fields(analysis)
        )

    def _generate_styles(self, analysis: Dict[str, Any]) -> str:
        """Generate CSS styles."""
        template = self.template_env.get_template("styles.jinja2")
        return template.render(fields=self._prepare_fields(analysis))

    def _generate_scripts(self, analysis: Dict[str, Any]) -> str:
        """Generate JavaScript code."""
        template = self.template_env.get_template("scripts.jinja2")
        return template.render(
            validation_rules=analysis.get("validation", {}),
            event_handlers=analysis.get("events", {})
        )

    def _generate_error_handlers(self, analysis: Dict[str, Any], language: str) -> str:
        """Generate error handling code."""
        template = self.template_env.get_template(f"error_handlers_{language}.jinja2")
        return template.render(validation_rules=analysis.get("validation", {}))

    def _generate_event_utilities(self, analysis: Dict[str, Any], language: str) -> str:
        """Generate event utility code."""
        template = self.template_env.get_template(f"event_utilities_{language}.jinja2")
        return template.render(event_handlers=analysis.get("events", {})) 