def parse_results(output) -> dict:
    """
    Parses the output from class GradeWithReasoning.to_message_format()

    Args:
        output (dict): A dictionary containing a 'grade_cv' key, which holds a list of
                       message dictionaries with 'role' and 'content' fields.

    Returns:
        dict: A dictionary with the following keys:
            - "numerical_score" (str): The numerical score assigned to the CV.
            - "reasoning" (str): The reasoning behind the assigned score.
            - "matching" (str): The qualifications that match the job requirements.
            - "not_matching" (str): The qualifications that do not match the job requirements.
    """
    key_map = {
        "Numerical score:": "numerical_score",
        "Reasoning:": "reasoning",
        "Matching qualifications:": "matching",
        "Not matching qualifications:": "not_matching"
    }

    # Extract the messages from the output
    messages = output.get("grade_cv", {}).get("messages", [])

    # Initialize the result dictionary with the desired keys
    result = {v: "" for v in key_map.values()}

    # Loop through the messages and populate the result dictionary
    for message in messages:
        content = message.get("content", "")
        for prefix, key in key_map.items():
            if content.startswith(prefix):
                result[key] = content.replace(prefix, "").strip()

    return result