from processing.llm_invoker import invoke_llm
from config.config_loader import model_cfg
from langchain_core.prompts import PromptTemplate

# data
developer_prompt = model_cfg['developer_prompt']


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

    prompt = PromptTemplate(
        template=developer_prompt,
        input_variables=["cv", "req_profile"],
    )
    scored_result = invoke_llm(prompt, cv, req_profile)

    return {"messages": [{"role": "system", "content": f"Numerical score: {scored_result.numerical_score}"},
                         {"role": "system", "content": f"Reasoning: {scored_result.reasoning}"}]}
