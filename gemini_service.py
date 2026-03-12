# ============================================
# gemini_service.py — Gemini API Integration
# ============================================
# This module handles all communication with
# Google's Gemini API for story generation.
# ============================================

import google.generativeai as genai
from config import GEMINI_API_KEY

# --- Configure the Gemini SDK with our API key ---
# This must happen once before any API calls.
genai.configure(api_key=GEMINI_API_KEY)

# --- Model Configuration ---
# gemini-2.0-flash: Fast, capable, supports image + text input.
MODEL_NAME = "gemini-2.0-flash"


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
        # Create a model instance.
        model = genai.GenerativeModel(MODEL_NAME)

        # Send both the prompt and image to Gemini.
        # The model processes them together — it "sees" the image
        # and "reads" the prompt to generate a response.
        response = model.generate_content([prompt, image])

        # Extract the text from the response.
        # response.text is a shortcut that joins all text parts.
        return (True, response.text)

    except ValueError as e:
        # Raised when the response is blocked by safety filters
        # or the content is flagged as inappropriate.
        return (False, f"Content was blocked by safety filters: {e}")

    except Exception as e:
        # Catch-all for any other errors:
        # - Invalid API key
        # - Network issues
        # - Rate limiting
        # - Unsupported image format
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
        model = genai.GenerativeModel(MODEL_NAME)

        caption_prompt = (
            "Describe this image in 2-3 detailed sentences. "
            "Focus on the key subjects, setting, mood, and any notable details."
        )

        response = model.generate_content([caption_prompt, image])
        return (True, response.text)

    except Exception as e:
        return (False, f"Error generating caption: {e}")