from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "email_prompt.txt")

def generate_email_body(customer, campaign):
    # Load prompt template
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Fill prompt with real data
    prompt = prompt_template.format(
        name=customer["name"],
        age=customer["age"],
        location=customer["location"],
        interests=customer["interests"],
        last_purchase=customer["last_purchase"],
        loyalty_score=customer["loyalty_score"],
        objective=campaign["objective"],
        tone=campaign["tone"]
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )

    return response.choices[0].message.content


