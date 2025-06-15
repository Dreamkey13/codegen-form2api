from typing import Dict, Optional, Any
import json
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from .base import BaseLLMInterface, LLMConfig, LLMResponse

class OpenAIInterface(BaseLLMInterface):
    """OpenAI-specific implementation of the LLM interface."""

    def _initialize_llm(self):
        """Initialize the OpenAI LLM with configuration."""
        self.llm = OpenAI(
            model_name=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            top_p=self.config.top_p,
            frequency_penalty=self.config.frequency_penalty,
            presence_penalty=self.config.presence_penalty
        )

    async def generate(self, prompt: str, context: Optional[Dict] = None) -> LLMResponse:
        """Generate a response from the OpenAI LLM."""
        try:
            # Format the prompt with context if provided
            formatted_prompt = self._format_prompt(prompt, **(context or {}))
            
            # Create a chain for the generation
            chain = LLMChain(
                llm=self.llm,
                prompt=PromptTemplate(
                    input_variables=["input"],
                    template="{input}"
                )
            )
            
            # Generate the response
            response = await chain.arun(input=formatted_prompt)
            
            # Update memory
            self._update_memory("last_prompt", formatted_prompt)
            self._update_memory("last_response", response)
            
            return LLMResponse(
                content=response,
                metadata={
                    "model": self.config.model_name,
                    "temperature": self.config.temperature,
                    "context": context
                }
            )
        except Exception as e:
            return LLMResponse(
                content="",
                metadata={},
                error=str(e)
            )

    async def analyze(self, data: Dict) -> LLMResponse:
        """Analyze data using the OpenAI LLM."""
        analysis_prompt = """
        Analyze the following data and provide insights:
        
        Data:
        {data}
        
        Please provide:
        1. Key observations
        2. Potential issues
        3. Recommendations
        4. Next steps
        """
        
        return await self.generate(
            analysis_prompt,
            context={"data": json.dumps(data, indent=2)}
        )

    async def validate(self, data: Dict) -> LLMResponse:
        """Validate data using the OpenAI LLM."""
        validation_prompt = """
        Validate the following data against these requirements:
        
        Data:
        {data}
        
        Requirements:
        1. Code follows best practices
        2. All necessary validations are present
        3. Error handling is implemented
        4. Security measures are in place
        
        Please provide:
        1. Validation results
        2. Issues found
        3. Suggestions for improvement
        """
        
        return await self.generate(
            validation_prompt,
            context={"data": json.dumps(data, indent=2)}
        )

    async def plan_migration(self, analysis: Dict) -> LLMResponse:
        """Plan the migration process using the OpenAI LLM."""
        planning_prompt = """
        Create a detailed migration plan based on the following analysis:
        
        Analysis:
        {analysis}
        
        Please provide:
        1. Step-by-step migration plan
        2. Required tools and their order
        3. Expected challenges
        4. Validation checkpoints
        5. Rollback strategy
        """
        
        return await self.generate(
            planning_prompt,
            context={"analysis": json.dumps(analysis, indent=2)}
        )

    async def review_code(self, code: str) -> LLMResponse:
        """Review generated code using the OpenAI LLM."""
        review_prompt = """
        Review the following code and provide feedback:
        
        Code:
        {code}
        
        Please check for:
        1. Code quality and style
        2. Potential bugs or issues
        3. Security vulnerabilities
        4. Performance considerations
        5. Best practices compliance
        """
        
        return await self.generate(
            review_prompt,
            context={"code": code}
        ) 