from pydantic import BaseModel, Field
from config.config_loader import model_cfg
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

# Data
developer_prompt = model_cfg['developer_prompt']
model_name = model_cfg['model_name']
temperature = model_cfg['temperature']
ollama_format = model_cfg['ollama_format']


class GradeWithReasoning(BaseModel):
    numerical_score: str = Field(description="Relevance score from 1 to 5")
    reasoning: str = Field(description="Reasoning behind the score, be specific and explain thoroughly")
    matching: str = Field(description="Matching qualifications")
    not_matching: str = Field(description="Not matching qualifications")

    def to_message_format(self):
        container = {
            "messages": [
                {"role": "system", "content": f"Numerical score: {self.numerical_score}"},
                {"role": "system", "content": f"Reasoning: {self.reasoning}"},
                {"role": "system", "content": f"Matching qualifications: {self.matching}"},
                {"role": "system", "content": f"Not matching qualifications: {self.not_matching}"}
            ]
        }
        return container


def invoke_ollama(cv, req_profile):
    """
    Invokes a local Ollama model with a given CV and a requirement profile.

    Args:
        cv (str): The CV content
        req_profile (str): The job requirement profile content

    Returns:
        The invoked chain for parsing.
    """
    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", developer_prompt),
            ("human", "Retrieved CV: \n\n {cv} \n\n Requirement Profile: \n\n {context}"),
        ]
    )

    # Chain
    llm = ChatOllama(model=model_name, format=ollama_format, temperature=temperature)
    # llm = ChatOpenAI(temperature=0, streaming=True, model="gpt-4o")
    structured_llm = llm.with_structured_output(GradeWithReasoning)
    chain = grade_prompt | structured_llm

    return chain.invoke({"cv": cv, "context": req_profile})