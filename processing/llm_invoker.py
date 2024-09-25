from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from config.config_loader import model_cfg

# Data
model_name = model_cfg['model_name']
temperature = model_cfg['temperature']
streaming = model_cfg['streaming']


class GradeWithReasoning(BaseModel):
    """Numerical score and reasoning for relevance check."""
    numerical_score: str = Field(description="Relevance score from 1 to 5")
    reasoning: str = Field(description="Reasoning behind the score")


def invoke_llm(prompt, cv, req_profile):
    """
    Invokes the LLM model with a given prompt, CV, and requirement profile.

    Args:
        prompt (PromptTemplate): The developer prompt
        cv (str): The CV content
        req_profile (str): The job requirement profile content

    Returns:
        GradeWithReasoning: The parsed result containing the score and reasoning
    """

    model = ChatOpenAI(temperature=temperature, model=model_name, streaming=streaming)

    # Chain the prompt to the LLM with validation
    llm = model.with_structured_output(GradeWithReasoning)
    chain = prompt | llm

    return chain.invoke({"cv": cv, "context": req_profile})
