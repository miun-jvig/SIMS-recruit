from langgraph.graph.message import add_messages
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
# NOTE: you must use langchain-core >= 0.3 with Pydantic v2
from pydantic import BaseModel, Field


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


def grade_cv(state) -> dict:
    """
    Scores a CV based on a scale from 1 to 5 and provides reasoning.

    Args:
        state (messages): The current state

    Returns:
        dict: A grade from 1 to 5 and reasoning for the grade
    """
    print("---CHECK RELEVANCE---")

    # Data model for numerical grading with reasoning
    class GradeWithReasoning(BaseModel):
        """Numerical score and reasoning for relevance check."""
        numerical_score: int = Field(description="Relevance score from 1 to 5")
        reasoning: str = Field(description="Reasoning behind the score")

    # LLM setup
    model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", streaming=True)

    # LLM with tool and validation
    llm = model.with_structured_output(GradeWithReasoning)

    # Prompt with reasoning
    prompt = PromptTemplate(
        template="""You are grading how well a CV fits a requirement profile for a job. \n Here is the CV: \n\n {cv} 
        \n Here is the requirement profile: \n\n {context} \n Based on how well the candidate fits the requirement 
        profile, grade the CV on a scale from 1 to 5, where 1 fits the least and 5 fits the most. Also, explain your 
        reasoning for the score.""",
        input_variables=["cv", "context"],
    )

    # Chain the prompt to the LLM with validation
    chain = prompt | llm

    messages = state["messages"]

    # Access content directly from dictionary key
    cv = messages[0]["content"]
    req_profile = messages[1]["content"]

    # Invoke the LLM with the document and question
    scored_result = chain.invoke({"cv": cv, "context": req_profile})

    # Extract the numerical score and reasoning
    score = scored_result.numerical_score
    reasoning = scored_result.reasoning

    print(f"---DECISION: CV GRADED WITH SCORE {score}/5---")
    print(f"---REASONING: {reasoning}---")

    return {"score": score, "reasoning": reasoning}


def agent(state):
    """
        Invokes the agent model to generate a response based on the current state. Given
        the question, it will decide to retrieve using the retriever tool, or simply end.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the agent response appended to messages
        """
    print("---CALL AGENT---")
    messages = state["messages"]
    model = ChatOpenAI(temperature=0, streaming=True, model="gpt-3.5-turbo")
    # model = model.bind_tools(tools) <- potential to bind tools here, but not sure if it's even needed
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}
