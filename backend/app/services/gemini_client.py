import os
from google import genai
from backend.app.config import settings

# Configure Gemini API
api_key = getattr(settings, "GOOGLE_API_KEY", None) or os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)


def generate_response(prompt: str, model_name: str = "gemini-3.5-flash") -> str:
    """
    Utility function to generate LLM responses using Google Gemini API.
    """
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating response from Gemini API: {str(e)}"