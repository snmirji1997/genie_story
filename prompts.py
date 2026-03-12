# ============================================
# prompts.py — Prompt Templates for Gemini
# ============================================
# This module builds the text prompts sent to
# Gemini alongside the uploaded image.
# ============================================


def build_story_prompt(category, instructions="", length="Medium", tone="Dramatic"):
    """
    Build a structured prompt for story generation.

    Args:
        category (str): The story genre (e.g. "Fantasy", "Horror").
        instructions (str): Optional extra instructions from the user.
        length (str): Story length — "Short", "Medium", or "Long".
        tone (str): Writing tone — "Dark", "Lighthearted", etc.

    Returns:
        str: The complete prompt to send to Gemini.
    """

    # Map length labels to approximate word counts.
    length_map = {
        "Short": "150-250 words",
        "Medium": "400-600 words",
        "Long": "800-1200 words",
    }
    word_count = length_map.get(length, "400-600 words")

    # Map tones to descriptive writing guidance.
    # This gives the model a richer understanding of what we want
    # instead of just a single adjective.
    tone_map = {
        "Dramatic": "emotionally intense with high stakes and powerful moments",
        "Lighthearted": "fun, warm, and optimistic with a feel-good ending",
        "Dark": "gritty, atmospheric, and unsettling with an ominous mood",
        "Humorous": "witty, playful, and laugh-out-loud funny",
        "Suspenseful": "tense and gripping with cliffhangers and unexpected twists",
        "Whimsical": "magical, quirky, and full of wonder and imagination",
    }
    tone_description = tone_map.get(tone, tone)

    # --- Build the prompt ---
    prompt = f"""You are a master storyteller and creative writer.

TASK:
Look at the provided image carefully. Write an original {category} story 
inspired by what you see in the image.

GENRE: {category}
TONE: The writing style should be {tone_description}.
LENGTH: Approximately {word_count}.

RULES:
- The story MUST be in the {category} genre.
- Maintain the {tone} tone consistently throughout.
- Include vivid descriptions and engaging dialogue where appropriate.
- The story must have a clear beginning, middle, and ending.
- Start with a creative title on its own line, prefixed with "Title: ".
- Then write the story below the title.
"""

    # Append user instructions if provided.
    if instructions.strip():
        prompt += f"""
ADDITIONAL INSTRUCTIONS FROM THE USER:
{instructions.strip()}
"""

    return prompt


def build_caption_prompt():
    """
    Build a prompt that asks Gemini to describe the image.
    Used in Phase 4 to generate a caption before the story.

    Returns:
        str: The caption prompt.
    """

    return """Describe this image in 2-3 detailed sentences. 
Focus on the key subjects, setting, mood, and any notable details. 
Be specific and vivid in your description."""