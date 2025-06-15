from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import logging
from .base import BaseLLMInterface, LLMResponse
from ..tools.base import BaseTool, ToolRegistry, ToolResult

logger = logging.getLogger(__name__)

class OrchestrationStep:
    def __init__(
        self,
        name: str,
        description: str,
        tool_name: Optional[str] = None,
        tool_params: Optional[Dict[str, Any]] = None,
        llm_prompt: Optional[str] = None,
        required: bool = True
    ):
        self.name = name
        self.description = description
        self.tool_name = tool_name
        self.tool_params = tool_params or {}
        self.llm_prompt = llm_prompt
        self.required = required
        self.result: Optional[Any] = None
        self.error: Optional[str] = None

class OrchestrationPlan:
    def __init__(self, steps: List[OrchestrationStep]):
        self.steps = steps
        self.current_step_index = 0
        self.results: Dict[str, Any] = {}
        self.errors: Dict[str, str] = {}

    def add_result(self, step_name: str, result: Any):
        self.results[step_name] = result

    def add_error(self, step_name: str, error: str):
        self.errors[step_name] = error

    def get_next_step(self) -> Optional[OrchestrationStep]:
        if self.current_step_index < len(self.steps):
            step = self.steps[self.current_step_index]
            self.current_step_index += 1
            return step
        return None

    def is_complete(self) -> bool:
        return self.current_step_index >= len(self.steps)

class BaseOrchestrator(ABC):
    def __init__(
        self,
        llm: BaseLLMInterface,
        tool_registry: ToolRegistry,
        max_retries: int = 3
    ):
        self.llm = llm
        self.tool_registry = tool_registry
        self.max_retries = max_retries
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def create_plan(self, context: Dict[str, Any]) -> OrchestrationPlan:
        """Create an orchestration plan based on the given context."""
        pass

    async def execute_plan(self, plan: OrchestrationPlan) -> Dict[str, Any]:
        """Execute the orchestration plan and return the results."""
        while not plan.is_complete():
            step = plan.get_next_step()
            if not step:
                break

            try:
                if step.tool_name:
                    result = await self._execute_tool_step(step)
                elif step.llm_prompt:
                    result = await self._execute_llm_step(step)
                else:
                    raise ValueError(f"Step {step.name} has neither tool nor LLM prompt")

                plan.add_result(step.name, result)
            except Exception as e:
                self.logger.error(f"Error executing step {step.name}: {str(e)}")
                plan.add_error(step.name, str(e))
                if step.required:
                    break

        return {
            "results": plan.results,
            "errors": plan.errors,
            "success": len(plan.errors) == 0
        }

    async def _execute_tool_step(self, step: OrchestrationStep) -> Any:
        """Execute a tool-based step with retries."""
        tool = self.tool_registry.get_tool(step.tool_name)
        if not tool:
            raise ValueError(f"Tool {step.tool_name} not found")

        for attempt in range(self.max_retries):
            try:
                result = await tool.execute(step.tool_params)
                if result.success:
                    return result.data
                raise ValueError(result.error)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                self.logger.warning(f"Retry {attempt + 1} for step {step.name}")

    async def _execute_llm_step(self, step: OrchestrationStep) -> Any:
        """Execute an LLM-based step."""
        response = await self.llm.generate_response(step.llm_prompt)
        if not response.success:
            raise ValueError(response.error)
        return response.data

class FormMigrationOrchestrator(BaseOrchestrator):
    async def create_plan(self, context: Dict[str, Any]) -> OrchestrationPlan:
        """Create a plan for form migration."""
        steps = [
            OrchestrationStep(
                name="analyze_form",
                description="Analyze the form structure and requirements",
                tool_name="web_navigation",
                tool_params={"url": context["form_url"]}
            ),
            OrchestrationStep(
                name="validate_analysis",
                description="Validate the form analysis results",
                llm_prompt="Validate the following form analysis results: {analysis_results}"
            ),
            OrchestrationStep(
                name="generate_api",
                description="Generate API code based on form analysis",
                tool_name="code_generation",
                tool_params={
                    "template": "api_python_fastapi",
                    "form_data": "{analysis_results}"
                }
            ),
            OrchestrationStep(
                name="generate_form",
                description="Generate HTML form code",
                tool_name="code_generation",
                tool_params={
                    "template": "html_form",
                    "form_data": "{analysis_results}"
                }
            ),
            OrchestrationStep(
                name="validate_output",
                description="Validate the generated code",
                llm_prompt="Validate the following generated code: {generated_code}"
            )
        ]
        return OrchestrationPlan(steps)

    async def execute_plan(self, plan: OrchestrationPlan) -> Dict[str, Any]:
        """Execute the form migration plan with context passing between steps."""
        results = await super().execute_plan(plan)
        
        # Update context for subsequent steps
        for step in plan.steps:
            if step.name in results["results"]:
                # Replace placeholders in subsequent steps
                for next_step in plan.steps[plan.current_step_index:]:
                    if next_step.tool_params:
                        for key, value in next_step.tool_params.items():
                            if isinstance(value, str) and "{" in value:
                                next_step.tool_params[key] = value.format(
                                    **{step.name: results["results"][step.name]}
                                )
                    if next_step.llm_prompt and "{" in next_step.llm_prompt:
                        next_step.llm_prompt = next_step.llm_prompt.format(
                            **{step.name: results["results"][step.name]}
                        )

        return results 