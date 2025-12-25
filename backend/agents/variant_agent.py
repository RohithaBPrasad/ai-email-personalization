#AGENT DECISION EXPLANATION
from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def decide_variant_with_reason(stats):
    """
    stats example:
    [
      {"variant": "A", "open_rate": 0.6, "click_rate": 0.2},
      {"variant": "B", "open_rate": 0.4, "click_rate": 0.3}
    ]

    Returns:
        variant (str): "A" or "B"
        reason (str): short explanation of why this variant was chosen
    """

    prompt = f"""
You are an AI optimization agent.

Campaign stats:
{stats}

Instructions:
1. Choose the best variant (A or B)
2. Explain briefly why (1 sentence)

Format:
Variant: X
Reason: <text>
"""

    try:
        # Call the Groq LLM
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60
        )

        text = res.choices[0].message.content.strip()
        lines = text.splitlines()

        # Extract variant
        variant_line = next((l for l in lines if l.lower().startswith("variant:")), None)
        reason_line = next((l for l in lines if l.lower().startswith("reason:")), None)

        variant = variant_line.split(":")[1].strip().upper() if variant_line else "A"
        reason = reason_line.split(":", 1)[1].strip() if reason_line else "No reason provided"

        # Validate variant
        if variant not in ["A", "B"]:
            variant = "A"

        return variant, reason

    except Exception as e:
        # Fallback in case of any error
        print(f"Error in decide_variant_with_reason: {e}")
        return "A", "Defaulted due to error"
