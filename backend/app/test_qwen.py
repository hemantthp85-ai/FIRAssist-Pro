from models.qwen_loader import ask_qwen

prompt = """
What is FIR?
Answer in one sentence.
"""

result = ask_qwen(prompt)

print(result)