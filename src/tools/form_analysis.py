from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from .base import BaseTool, ToolConfig, ToolResult

class FormAnalysisTool(BaseTool):
    """Tool for analyzing form data and generating insights."""

    def __init__(self):
        super().__init__(
            ToolConfig(
                name="form_analysis",
                description="Analyzes form data and generates insights"
            )
        )

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        """Execute form analysis."""
        try:
            form_data = params["form_data"]
            
            # Analyze form structure
            structure_analysis = await self._analyze_structure(form_data)
            
            # Analyze validation rules
            validation_analysis = await self._analyze_validation(form_data)
            
            # Analyze event handlers
            event_analysis = await self._analyze_events(form_data)
            
            # Generate summary
            summary = await self._generate_summary(
                structure_analysis,
                validation_analysis,
                event_analysis
            )
            
            return ToolResult(
                success=True,
                data={
                    "structure": structure_analysis,
                    "validation": validation_analysis,
                    "events": event_analysis,
                    "summary": summary
                },
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "form_id": form_data.get("id", "unknown")
                }
            )
        except Exception as e:
            self.logger.error(f"Error in form analysis: {str(e)}")
            return ToolResult(
                success=False,
                data={},
                error=str(e)
            )

    async def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate the input parameters."""
        required_params = ["form_data"]
        return all(param in params for param in required_params)

    async def cleanup(self):
        """Clean up any resources."""
        pass

    async def _analyze_structure(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the form structure."""
        elements = form_data.get("elements", [])
        
        analysis = {
            "total_elements": len(elements),
            "element_types": {},
            "required_fields": [],
            "optional_fields": [],
            "field_dependencies": [],
            "form_groups": {}
        }
        
        for element in elements:
            # Count element types
            element_type = element.get("type", "unknown")
            analysis["element_types"][element_type] = analysis["element_types"].get(element_type, 0) + 1
            
            # Track required/optional fields
            if element.get("required"):
                analysis["required_fields"].append(element.get("name"))
            else:
                analysis["optional_fields"].append(element.get("name"))
            
            # Analyze field dependencies
            if element.get("dependencies"):
                analysis["field_dependencies"].append({
                    "field": element.get("name"),
                    "depends_on": element.get("dependencies")
                })
            
            # Group related fields
            field_group = element.get("group", "default")
            if field_group not in analysis["form_groups"]:
                analysis["form_groups"][field_group] = []
            analysis["form_groups"][field_group].append(element.get("name"))
        
        return analysis

    async def _analyze_validation(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze form validation rules."""
        validation_rules = form_data.get("validation_rules", {})
        
        analysis = {
            "client_side": {
                "total_rules": 0,
                "rule_types": {},
                "complex_validations": []
            },
            "server_side": {
                "total_rules": 0,
                "rule_types": {},
                "complex_validations": []
            }
        }
        
        # Analyze client-side validation
        client_rules = validation_rules.get("client_side", {})
        for form_id, rules in client_rules.items():
            for field, field_rules in rules.items():
                analysis["client_side"]["total_rules"] += len(field_rules)
                for rule_type, rule_value in field_rules.items():
                    if rule_value:
                        analysis["client_side"]["rule_types"][rule_type] = \
                            analysis["client_side"]["rule_types"].get(rule_type, 0) + 1
                        
                        if rule_type in ["pattern", "custom"]:
                            analysis["client_side"]["complex_validations"].append({
                                "field": field,
                                "type": rule_type,
                                "value": rule_value
                            })
        
        # Analyze server-side validation
        server_rules = validation_rules.get("server_side", {})
        for form_id, rules in server_rules.items():
            for field, field_rules in rules.items():
                analysis["server_side"]["total_rules"] += len(field_rules)
                for rule_type, rule_value in field_rules.items():
                    if rule_value:
                        analysis["server_side"]["rule_types"][rule_type] = \
                            analysis["server_side"]["rule_types"].get(rule_type, 0) + 1
                        
                        if rule_type in ["custom", "business"]:
                            analysis["server_side"]["complex_validations"].append({
                                "field": field,
                                "type": rule_type,
                                "value": rule_value
                            })
        
        return analysis

    async def _analyze_events(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze form event handlers."""
        event_handlers = form_data.get("event_handlers", {})
        
        analysis = {
            "client_side": {
                "total_handlers": 0,
                "handler_types": {},
                "complex_handlers": []
            },
            "server_side": {
                "total_handlers": 0,
                "handler_types": {},
                "complex_handlers": []
            }
        }
        
        # Analyze client-side events
        client_events = event_handlers.get("client_side", {})
        for form_id, handlers in client_events.items():
            for field, field_handlers in handlers.items():
                analysis["client_side"]["total_handlers"] += len(field_handlers)
                for handler_type in field_handlers:
                    analysis["client_side"]["handler_types"][handler_type] = \
                        analysis["client_side"]["handler_types"].get(handler_type, 0) + 1
                    
                    if handler_type in ["onchange", "onblur", "onkeyup"]:
                        analysis["client_side"]["complex_handlers"].append({
                            "field": field,
                            "type": handler_type
                        })
        
        # Analyze server-side events
        server_events = event_handlers.get("server_side", {})
        for form_id, handlers in server_events.items():
            for field, field_handlers in handlers.items():
                analysis["server_side"]["total_handlers"] += len(field_handlers)
                for handler_type in field_handlers:
                    analysis["server_side"]["handler_types"][handler_type] = \
                        analysis["server_side"]["handler_types"].get(handler_type, 0) + 1
                    
                    if handler_type in ["postback", "custom"]:
                        analysis["server_side"]["complex_handlers"].append({
                            "field": field,
                            "type": handler_type
                        })
        
        return analysis

    async def _generate_summary(self, structure: Dict[str, Any], validation: Dict[str, Any], events: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the form analysis."""
        return {
            "form_complexity": self._calculate_complexity(structure, validation, events),
            "migration_challenges": self._identify_challenges(structure, validation, events),
            "recommendations": self._generate_recommendations(structure, validation, events),
            "statistics": {
                "total_elements": structure["total_elements"],
                "total_validation_rules": validation["client_side"]["total_rules"] + validation["server_side"]["total_rules"],
                "total_event_handlers": events["client_side"]["total_handlers"] + events["server_side"]["total_handlers"]
            }
        }

    def _calculate_complexity(self, structure: Dict[str, Any], validation: Dict[str, Any], events: Dict[str, Any]) -> str:
        """Calculate the overall complexity of the form."""
        total_elements = structure["total_elements"]
        total_rules = validation["client_side"]["total_rules"] + validation["server_side"]["total_rules"]
        total_handlers = events["client_side"]["total_handlers"] + events["server_side"]["total_handlers"]
        
        complexity_score = (
            total_elements * 1 +
            total_rules * 2 +
            total_handlers * 3
        )
        
        if complexity_score < 10:
            return "low"
        elif complexity_score < 30:
            return "medium"
        else:
            return "high"

    def _identify_challenges(self, structure: Dict[str, Any], validation: Dict[str, Any], events: Dict[str, Any]) -> List[str]:
        """Identify potential migration challenges."""
        challenges = []
        
        # Structure challenges
        if structure["total_elements"] > 20:
            challenges.append("Large number of form elements")
        if structure["field_dependencies"]:
            challenges.append("Complex field dependencies")
        
        # Validation challenges
        if validation["client_side"]["complex_validations"]:
            challenges.append("Complex client-side validation rules")
        if validation["server_side"]["complex_validations"]:
            challenges.append("Complex server-side validation rules")
        
        # Event handling challenges
        if events["client_side"]["complex_handlers"]:
            challenges.append("Complex client-side event handlers")
        if events["server_side"]["complex_handlers"]:
            challenges.append("Complex server-side event handlers")
        
        return challenges

    def _generate_recommendations(self, structure: Dict[str, Any], validation: Dict[str, Any], events: Dict[str, Any]) -> List[str]:
        """Generate recommendations for migration."""
        recommendations = []
        
        # Structure recommendations
        if structure["total_elements"] > 20:
            recommendations.append("Consider splitting the form into multiple steps")
        if structure["field_dependencies"]:
            recommendations.append("Implement dependency management in the new form")
        
        # Validation recommendations
        if validation["client_side"]["complex_validations"]:
            recommendations.append("Migrate complex validations to a validation library")
        if validation["server_side"]["complex_validations"]:
            recommendations.append("Implement server-side validation using a framework")
        
        # Event handling recommendations
        if events["client_side"]["complex_handlers"]:
            recommendations.append("Use modern event handling patterns")
        if events["server_side"]["complex_handlers"]:
            recommendations.append("Implement proper API endpoints for server-side events")
        
        return recommendations 