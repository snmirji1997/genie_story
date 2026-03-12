# ============================================
# app.py — Genie Image Story Generator (Main)
# ============================================
# This is the Streamlit UI that ties together
# config, prompts, and gemini_service modules.
# ============================================

import io
import streamlit as st
from PIL import Image

from config import (
    GEMINI_API_KEY,
    STORY_CATEGORIES,
    STORY_TONES,
    MAX_IMAGE_SIZE_MB,
    ALLOWED_IMAGE_TYPES,
)
from prompts import build_story_prompt
from gemini_service import generate_story


# --- Page Configuration ---
st.set_page_config(
    page_title="Genie Image Story Generator",
    page_icon="🧞",
    layout="centered",
)

# --- Initialize Session State ---
# session_state persists across Streamlit reruns.
# Without this, the generated story would disappear
# every time the user changes a sidebar setting.
if "generated_story" not in st.session_state:
    st.session_state.generated_story = None


def validate_image(uploaded_file):
    """
    Validate the uploaded image file.

    Args:
        uploaded_file: The file object from st.file_uploader.

    Returns:
        tuple: (is_valid: bool, message: str)
    """

    max_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
    if uploaded_file.size > max_bytes:
        return (False, f"Image too large. Maximum size is {MAX_IMAGE_SIZE_MB}MB.")

    file_extension = uploaded_file.type.split("/")[-1].lower()
    if file_extension not in ALLOWED_IMAGE_TYPES:
        allowed = ", ".join(ALLOWED_IMAGE_TYPES)
        return (False, f"Unsupported format. Allowed types: {allowed}")

    return (True, "Image is valid.")


def display_header():
    """Display the app title and description."""

    st.title("🧞 Genie Image Story Generator")
    st.markdown(
        "Upload an image, choose a genre, and let AI craft a unique story for you."
    )
    st.divider()


def display_sidebar():
    """
    Display sidebar with controls and return user selections.

    Returns:
        tuple: (category: str, length: str, tone: str, instructions: str)
    """

    with st.sidebar:
        st.header("⚙️ Story Settings")

        # --- Category Selection ---
        # Add "Custom" as the last option so users can type their own genre.
        category_options = STORY_CATEGORIES + ["Custom"]

        selected_category = st.selectbox(
            "Choose a genre:",
            options=category_options,
            index=0,
        )

        # If "Custom" is selected, show a text input for the custom genre.
        # Otherwise, use the selected value from the dropdown.
        if selected_category == "Custom":
            category = st.text_input(
                "Enter your custom genre:",
                placeholder="e.g., Steampunk Western, Bollywood Thriller...",
            )
            # If user selected Custom but hasn't typed anything yet,
            # default to "Fantasy" to avoid sending an empty genre.
            if not category.strip():
                category = "Fantasy"
        else:
            category = selected_category

        # --- Tone Selection ---
        tone = st.selectbox(
            "Story tone:",
            options=STORY_TONES,
            index=0,
        )

        # --- Story Length ---
        length = st.selectbox(
            "Story length:",
            options=["Short", "Medium", "Long"],
            index=1,
        )

        # --- Extra Instructions ---
        instructions = st.text_area(
            "Additional instructions (optional):",
            placeholder="e.g., Include a talking cat, set it in ancient Egypt...",
            height=120,
        )

        st.divider()
        st.markdown("Built with 🧞 Gemini + Streamlit")

    return category, length, tone, instructions


def display_story(story):
    """
    Display the generated story with formatting.

    Args:
        story (str): The generated story text.
    """

    st.divider()
    st.subheader("📖 Your Generated Story")
    st.markdown(story)

    # Download button lets the user save the story as a text file.
    # st.download_button handles file creation automatically.
    st.download_button(
        label="📥 Download Story",
        data=story,
        file_name="genie_story.txt",
        mime="text/plain",
    )


def main():
    """Main application flow."""

    # --- Check API Key ---
    if not GEMINI_API_KEY:
        st.error("⚠️ Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
        st.stop()

    # --- Display header and sidebar ---
    display_header()
    category, length, tone, instructions = display_sidebar()

    # --- Image Upload ---
    uploaded_file = st.file_uploader(
        "Upload an image to inspire your story:",
        type=ALLOWED_IMAGE_TYPES,
        help=f"Max size: {MAX_IMAGE_SIZE_MB}MB. Formats: {', '.join(ALLOWED_IMAGE_TYPES)}",
    )

    # --- Process uploaded image ---
    if uploaded_file is not None:

        # Validate the image.
        is_valid, message = validate_image(uploaded_file)
        if not is_valid:
            st.error(message)
            st.stop()

        # Open the image with Pillow.
        image = Image.open(io.BytesIO(uploaded_file.read()))

        # Display the uploaded image.
        st.image(image, caption="Your uploaded image", use_container_width=True)

        # --- Generate Story Button ---
        if st.button("🧞 Generate Story", type="primary", use_container_width=True):

            # Build prompt with all settings including tone.
            prompt = build_story_prompt(category, instructions, length, tone)

            with st.spinner("🧞 The Genie is crafting your story..."):
                success, result = generate_story(image, prompt)

            if success:
                # Store in session_state so it survives reruns.
                st.session_state.generated_story = result
                st.success("Story generated successfully!")
            else:
                st.session_state.generated_story = None
                st.error(result)

        # --- Display story from session state ---
        # This shows the story even after sidebar changes trigger a rerun.
        if st.session_state.generated_story:
            display_story(st.session_state.generated_story)

    else:
        # Reset story when image is removed.
        st.session_state.generated_story = None
        st.info("👆 Upload an image above to get started!")


if __name__ == "__main__":
    main()