from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "evaluator_prompt.txt")

def evaluate_email(subject, body):
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = template.format(subject=subject, body=body)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )

    try:
        score = float(response.choices[0].message.content.strip())
    except:
        score = 0.7

    return score

