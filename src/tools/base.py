from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel
import logging

class ToolConfig(BaseModel):
    """Configuration for a tool."""
    name: str
    description: str
    enabled: bool = True
    timeout: int = 30
    retry_count: int = 3
    retry_delay: int = 1

class ToolResult(BaseModel):
    """Standardized tool execution result."""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}

class BaseTool(ABC):
    """Base interface for all tools."""
    
    def __init__(self, config: ToolConfig):
        self.config = config
        self.logger = logging.getLogger(f"tool.{config.name}")

    @abstractmethod
    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        """Execute the tool with the given parameters and context."""
        pass

    @abstractmethod
    async def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate the input parameters."""
        pass

    @abstractmethod
    async def cleanup(self):
        """Clean up any resources used by the tool."""
        pass

    def _log_execution(self, params: Dict[str, Any], result: ToolResult):
        """Log tool execution details."""
        self.logger.info(
            f"Tool execution: {self.config.name}",
            extra={
                "params": params,
                "success": result.success,
                "error": result.error
            }
        )

class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self.logger = logging.getLogger("tool_registry")

    def register(self, tool: BaseTool):
        """Register a new tool."""
        if tool.config.name in self._tools:
            raise ValueError(f"Tool {tool.config.name} is already registered")
        self._tools[tool.config.name] = tool
        self.logger.info(f"Registered tool: {tool.config.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())

    async def execute_tool(self, name: str, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        """Execute a tool by name."""
        tool = self.get_tool(name)
        if not tool:
            return ToolResult(
                success=False,
                data={},
                error=f"Tool {name} not found"
            )
        
        if not tool.config.enabled:
            return ToolResult(
                success=False,
                data={},
                error=f"Tool {name} is disabled"
            )
        
        try:
            if not await tool.validate_params(params):
                return ToolResult(
                    success=False,
                    data={},
                    error=f"Invalid parameters for tool {name}"
                )
            
            result = await tool.execute(params, context)
            tool._log_execution(params, result)
            return result
        except Exception as e:
            self.logger.error(f"Error executing tool {name}: {str(e)}")
            return ToolResult(
                success=False,
                data={},
                error=str(e)
            ) 