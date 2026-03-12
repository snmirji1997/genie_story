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

# --- Create a Client ---
# The new SDK uses a Client object instead of module-level configure().
# All API calls go through this client instance.
client = genai.Client(api_key=GEMINI_API_KEY)

# --- Model Configuration ---
MODEL_NAME = "gemini-2.5-flash"


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
        # Generate content by passing the prompt and image together.
        # The new SDK accepts them directly in a list.
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                temperature=0.8,        # Higher = more creative
                max_output_tokens=8192, # Room for longer stories
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
    Used in Phase 4 to caption the image before story generation.

    Args:
        image (PIL.Image): The uploaded image.

    Returns:
        tuple: (success: bool, result: str)
    """

    try:
        caption_prompt = (
            "Describe this image in 2-3 detailed sentences. "
            "Focus on the key subjects, setting, mood, and any notable details."
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[caption_prompt, image],
            config=types.GenerateContentConfig(
                temperature=0.4,        # Lower = more factual for captions
                max_output_tokens=256,  # Captions are short
            ),
        )

        return (True, response.text)

    except Exception as e:
        return (False, f"Error generating caption: {e}")