from utils.setup import set_env
from agent.rag import grade_cv


def main():
    # GET DOCUMENT FROM FASTAPI #
    # For now, we'll manually load two "documents" below until API is fixed
    state = {
        "messages": [
            {"content": "This is a sample CV. The candidate has 5 years of Java experience and 3 years of system "
                        "design."},
            {"content": "The job requires 4+ years of Java and experience in system architecture."}
        ]
    }

    grade_result = grade_cv(state)
    print("Grading Result:")
    print(grade_result)


if __name__ == '__main__':
    main()
