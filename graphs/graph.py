from graphs.nodes import grade_cv
from langgraph.graph import StateGraph, START, END
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


def create_workflow():
    """
    Creates a workflow graph according to LangGraph. Currently only has one node.

    Returns:
        The compiled graph.
    """
    workflow = StateGraph(AgentState)
    workflow.add_node("grade_cv", grade_cv)
    workflow.add_edge(START, "grade_cv")
    workflow.add_edge("grade_cv", END)
    # Can add more nodes (or conditional nodes if needed)
    return workflow.compile()


def process_graph(state):
    """
    Processes the graph and extracts numerical score and reasoning from the output.

    Args:
        state (dict): The current state

    Returns:
        dict: A dictionary containing the numerical score and reasoning
    """
    graph = create_workflow()
    output = None

    for output in graph.stream(state):
        print(output)

    return output