from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "subject_prompt.txt")

def generate_subject(customer, campaign):
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = template.format(
        name=customer["name"],
        interests=customer["interests"],
        last_purchase=customer["last_purchase"],
        objective=campaign["objective"],
        tone=campaign["tone"]
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80
    )

    return response.choices[0].message.content



