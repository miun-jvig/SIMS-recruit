from agent.llm_nodes import grade_cv
from langgraph.graph import StateGraph, START, END
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from processing.result_parser import parse_results


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


def create_workflow():
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

    final_result = parse_results(output)

    return final_result
