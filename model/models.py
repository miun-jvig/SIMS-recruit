from pydantic import BaseModel, Field
from config.config_loader import model_cfg
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

# Data
developer_prompt = model_cfg['developer_prompt']
model_name = model_cfg['model_name']
temperature = model_cfg['temperature']
ollama_format = model_cfg['ollama_format']


class GradeWithReasoning(BaseModel):
    """Numerical score and reasoning for relevance check."""
    numerical_score: str = Field(description="Relevance score from 1 to 5")
    reasoning: str = Field(description="Reasoning behind the score")


def invoke_ollama(cv, req_profile):
    """
    Invokes a local Ollama model with a given CV and a requirement profile.

    Args:
        cv (str): The CV content
        req_profile (str): The job requirement profile content

    Returns:
        The invoked chain for parsing.
    """
    prompt = PromptTemplate(
        template=developer_prompt,
        input_variables=["cv", "context"],
    )

    # Chain
    llm = ChatOllama(model=model_name, format=ollama_format, temperature=temperature)
    structured_llm = llm.with_structured_output(GradeWithReasoning)
    chain = prompt | structured_llm

    return chain.invoke({"cv": cv, "context": req_profile})