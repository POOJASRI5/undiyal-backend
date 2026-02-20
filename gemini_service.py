import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
]


def generate_content(prompt_or_contents):

    for key in API_KEYS:
        try:
            client = genai.Client(api_key=key)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_or_contents,
            )

            return response.text

        except Exception:
            continue

    return "AI service temporarily unavailable."


# -------- Bill OCR --------
def extract_from_image(image):
    return generate_content([
        "Extract merchant, amount, date and category from this bill.",
        image
    ])


# -------- Smart Suggestions --------
def get_saving_suggestions(prompt):
    return generate_content([prompt])