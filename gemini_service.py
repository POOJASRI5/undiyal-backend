import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_from_image(image):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=["Extract bill details", image],
    )
    return response.text

