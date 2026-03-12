# ============================================
# prompts.py — Prompt Templates for Gemini
# ============================================
# This module builds the text prompts sent to
# Gemini alongside the uploaded image.
# ============================================

def build_story_prompt(category, instructions="",length="medium"):
    """
    Build a structured promt for story generation

    args:
        category (str): The story category (e.g., "Fantasy", "Horror").
        instructions (str): Additional user instructions for the story.
        length (str): Desired story length ("short", "medium", "long").

    returns:
        str: A completed formatted prompt string ready to be sent to Gemini.    
    """

    # Map length labels to approximate word counts.
    # This gives the model a concrete target instead of a vague instruction.
    length_map = {
        "Short": "150-250 words",
        "Medium": "400-600 words",
        "Long": "800-1200 words",
    }
    word_count = length_map.get(length, "400-600 words")  # Default to medium if invalid

    promt = f"""You are a creative  & master storyteller
    TASK:
    Look at the image carefully. Write an original {category} story inspired by what you see in the image.

    RULES:
    - THE STORY MUST BE IN THE {category} GENRE.
    - The story should be between {word_count}.
    - Use vivid descriptions and engaging language to bring the story to life.
    - The story should be coherent and have a clear beginning, middle, and end.
    - Start with a creative title on its own line, prefixed with "Title: ".
    - Then write the story below the title, separated by a blank line.
    """

        # --- Append user instructions if provided ---
    # .strip() removes leading/trailing whitespace so we don't
    # add an empty section if the user left the text box blank.

    if instructions.strip():
        promt += f"\n\nADDITIONAL INSTRUCTIONS:\n{instructions.strip()}"

    return promt

def build_caption_prompt():
    """
    Build a prompt that asks Gemini to describe the image.
    We will use this in Phase 4 to generate a caption before the story.

    Returns:
        str: The caption prompt.
    """

    return """Describe this image in 2-3 detailed sentences. 
Focus on the key subjects, setting, mood, and any notable details. 
Be specific and vivid in your description."""
