from backend.app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import timed_agent


@timed_agent("answer_agent.function")
def process_answer(question, answer):

    prompt = f"""
You are a Tamil Nadu Police FIR Assistant.

Question:
{question}

Citizen Answer:
{answer}

Return ONLY JSON.

Example:

{{
    "vehicle_number":"TN38AB1234"
}}
"""

    response = ask_qwen(prompt)

    return response


if __name__ == "__main__":

    question = "What is the vehicle registration number?"

    answer = "TN38AB1234"

    print(process_answer(question, answer))
