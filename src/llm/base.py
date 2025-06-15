from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel
from langchain.llms import BaseLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class LLMConfig(BaseModel):
    """Configuration for LLM integration."""
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

class LLMResponse(BaseModel):
    """Standardized LLM response format."""
    content: str
    metadata: Dict[str, Any]
    error: Optional[str] = None

class BaseLLMInterface(ABC):
    """Base interface for LLM interactions."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.memory = ConversationBufferMemory()
        self._initialize_llm()

    @abstractmethod
    def _initialize_llm(self):
        """Initialize the LLM with configuration."""
        pass

    @abstractmethod
    async def generate(self, prompt: str, context: Optional[Dict] = None) -> LLMResponse:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    async def analyze(self, data: Dict) -> LLMResponse:
        """Analyze data and provide insights."""
        pass

    @abstractmethod
    async def validate(self, data: Dict) -> LLMResponse:
        """Validate data against requirements."""
        pass

    def _format_prompt(self, template: str, **kwargs) -> str:
        """Format a prompt template with provided variables."""
        prompt = PromptTemplate(
            input_variables=list(kwargs.keys()),
            template=template
        )
        return prompt.format(**kwargs)

    def _update_memory(self, key: str, value: Any):
        """Update the conversation memory."""
        self.memory.save_context({"input": key}, {"output": str(value)})

    def _get_memory(self) -> Dict:
        """Get the current conversation memory."""
        return self.memory.load_memory_variables({}) 