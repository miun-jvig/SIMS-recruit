from model.models import invoke_ollama


def grade_cv(state) -> dict:
    """
    Scores a CV based on a scale from 1 to 5 and provides reasoning.

    Args:
        state (messages): The current state

    Returns:
        dict: A grade from 1 to 5 and reasoning for the grade
    """
    print("---CHECK RELEVANCE---")

    messages = state["messages"]
    cv = messages[0]
    req_profile = messages[-1]

    # Invoke_ollama returns a GradeWithReasoning class as defined in model/models.py
    scored_result = invoke_ollama(cv, req_profile)
    # Convert to "messages"/the AgentState created in graphs/graph.py, which the LLM understands
    llm_message = scored_result.to_message_format()

    return llm_message