# ============================================
# gemini_service.py — Gemini API Integration
# ============================================
# This module handles all communication with
# Google's Gemini API for story generation.
# Uses the new google-genai SDK.
# ============================================

from google import genai
from google.genai import types
from config import GEMINI_API_KEY

# --- Model Configuration ---
MODEL_NAME = "gemini-2.5-flash"

# --- Lazy Client ---
# We don't create the client at import time because on Streamlit Cloud,
# st.secrets may not be ready yet when the module first loads.
# Instead, we create it on the first API call and reuse it after that.
_client = None


def _get_client():
    """
    Get or create the Gemini client.
    This pattern is called 'lazy initialization' — the client is
    only created when it's first needed, not at import time.

    Returns:
        genai.Client: The configured Gemini client.
    """

    global _client
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def generate_story(image, prompt):
    """
    Send an image and prompt to Gemini and return the generated story.

    Args:
        image (PIL.Image): The uploaded image opened with Pillow.
        prompt (str): The story generation prompt from prompts.py.

    Returns:
        tuple: (success: bool, result: str)
            - On success: (True, generated_story_text)
            - On failure: (False, error_message)
    """

    try:
        client = _get_client()

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                temperature=0.8,
                max_output_tokens=8192,
            ),
        )

        return (True, response.text)

    except ValueError as e:
        return (False, f"Content was blocked by safety filters: {e}")

    except Exception as e:
        return (False, f"Error generating story: {e}")


def generate_caption(image):
    """
    Generate a short description of the image.

    Args:
        image (PIL.Image): The uploaded image.

    Returns:
        tuple: (success: bool, result: str)
    """

    try:
        client = _get_client()

        caption_prompt = (
            "Describe this image in 2-3 detailed sentences. "
            "Focus on the key subjects, setting, mood, and any notable details."
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[caption_prompt, image],
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=256,
            ),
        )

        return (True, response.text)

    except Exception as e:
        return (False, f"Error generating caption: {e}")