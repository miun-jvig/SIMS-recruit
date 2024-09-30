def parse_results(output) -> dict:
    """
    Parses the output from the graph to extract numerical score and reasoning.

    Args:
        output (dict): The output of the graph stream containing messages

    Returns:
        dict: A dictionary containing the numerical score and reasoning
    """

    # Directly return the score and reasoning if the output is already in final form
    if 'numerical_score' in output and 'reasoning' in output:
        return {
            "numerical_score": output['numerical_score'],
            "reasoning": output['reasoning']
        }

    # Safely access the 'grade_cv' and 'messages' keys
    messages = output.get("grade_cv", {}).get("messages", [])

    if not messages:
        print("No messages found in the output!")
        return {
            "numerical_score": "N/A",
            "reasoning": "No reasoning provided."
        }

    numerical_score = None
    reasoning = None

    for message in messages:
        if "Numerical score" in message["content"]:
            numerical_score = message["content"].split(": ")[1]  # Get the score part
        elif "Reasoning" in message["content"]:
            reasoning = message["content"].split(": ", 1)[1]  # Get the reasoning part

    return {
        "numerical_score": numerical_score,
        "reasoning": reasoning
    }