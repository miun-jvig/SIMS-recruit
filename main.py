from graphs.graph import process_graph
from processing.result_parser import parse_results


def main():
    # GET DOCUMENT FROM FASTAPI #
    # For now, we'll manually load two "documents" below until API is fixed
    state = {
        "messages": [
            ("user", "This is a sample CV. The candidate has 5 years of Java experience and 3 years of system design."),
            ("user", "The job requires 4+ years of Java and experience in system architecture.")
        ]
    }

    result = process_graph(state) # Dict with numerical score + reasoning, for API
    print(f"---DECISION: CV GRADED WITH SCORE {result['numerical_score']}/5---")
    print(f"---REASONING: {result['reasoning']}---")


if __name__ == '__main__':
    main()
