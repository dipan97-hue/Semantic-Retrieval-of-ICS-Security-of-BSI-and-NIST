import google.generativeai as genai
from config.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-3.1-flash-lite')

def generate_gemini(prompt):
    response = model.generate_content(
        contents=prompt,
        generation_config=genai.GenerationConfig(temperature=0.2)
    )

    return response.text