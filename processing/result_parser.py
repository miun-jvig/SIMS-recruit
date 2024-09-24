def parse_results(output) -> dict:
    """
    Parses the output from the graph to extract numerical score and reasoning.

    Args:
        output (dict): The output of the graph stream containing messages

    Returns:
        dict: A dictionary containing the numerical score and reasoning
    """
    # Access the messages inside 'grade_cv'
    messages = output["grade_cv"]["messages"]

    # Extract the numerical score and reasoning from the messages
    numerical_score = None
    reasoning = None

    for message in messages:
        if "Numerical score" in message["content"]:
            numerical_score = message["content"].split(": ")[1]  # Get the score part
        elif "Reasoning" in message["content"]:
            reasoning = message["content"].split(": ", 1)[1]  # Get the reasoning part

    # Return both score and reasoning
    return {
        "numerical_score": numerical_score,
        "reasoning": reasoning
    }
