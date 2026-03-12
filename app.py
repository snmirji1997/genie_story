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
from gemini_service import generate_story, generate_caption


# --- Page Configuration ---
st.set_page_config(
    page_title="Genie Image Story Generator",
    page_icon="🧞",
    layout="centered",
)

# --- Initialize Session State ---
# Store both the story and caption so they persist across reruns.
if "generated_story" not in st.session_state:
    st.session_state.generated_story = None
if "generated_caption" not in st.session_state:
    st.session_state.generated_caption = None


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
        tuple: (category: str, length: str, tone: str, instructions: str, use_caption: bool)
    """

    with st.sidebar:
        st.header("⚙️ Story Settings")

        # --- Category Selection ---
        category_options = STORY_CATEGORIES + ["Custom"]

        selected_category = st.selectbox(
            "Choose a genre:",
            options=category_options,
            index=0,
        )

        if selected_category == "Custom":
            category = st.text_input(
                "Enter your custom genre:",
                placeholder="e.g., Steampunk Western, Bollywood Thriller...",
            )
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

        # --- Image Captioning Toggle ---
        # st.toggle creates an on/off switch.
        # When enabled, the app generates a caption before the story.
        use_caption = st.toggle(
            "Generate image caption first",
            value=True,
            help="AI describes the image first, then uses that description to write a richer story.",
        )

        # --- Extra Instructions ---
        instructions = st.text_area(
            "Additional instructions (optional):",
            placeholder="e.g., Include a talking cat, set it in ancient Egypt...",
            height=120,
        )

        st.divider()
        st.markdown("Built with 🧞 Gemini + Streamlit")

    return category, length, tone, instructions, use_caption


def display_story(story, caption=None):
    """
    Display the generated caption and story with formatting.

    Args:
        story (str): The generated story text.
        caption (str): The generated image caption (optional).
    """

    st.divider()

    # Show the caption if it exists.
    # An expander hides the caption by default to keep the UI clean,
    # but the user can click to see what the AI "saw" in the image.
    if caption:
        with st.expander("🔍 AI Image Caption (click to view)", expanded=False):
            st.markdown(f"*{caption}*")

    st.subheader("📖 Your Generated Story")
    st.markdown(story)

    # Download button — includes the caption at the top of the file if available.
    download_text = ""
    if caption:
        download_text += f"[Image Caption]\n{caption}\n\n---\n\n"
    download_text += story

    st.download_button(
        label="📥 Download Story",
        data=download_text,
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
    category, length, tone, instructions, use_caption = display_sidebar()

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

            caption = ""

            # --- Step 1: Caption (if enabled) ---
            # This is the first call in our two-step AI pipeline.
            if use_caption:
                with st.spinner("🔍 Analyzing the image..."):
                    cap_success, cap_result = generate_caption(image)

                if cap_success:
                    caption = cap_result
                    st.session_state.generated_caption = caption
                else:
                    # Caption failed, but we can still try story generation
                    # without the caption. Show a warning, not an error.
                    st.warning(f"Caption generation failed: {cap_result}. Continuing without caption.")
                    caption = ""
                    st.session_state.generated_caption = None
            else:
                st.session_state.generated_caption = None

            # --- Step 2: Story Generation ---
            # The caption (if available) is injected into the prompt.
            prompt = build_story_prompt(category, instructions, length, tone, caption)

            with st.spinner("🧞 The Genie is crafting your story..."):
                success, result = generate_story(image, prompt)

            if success:
                st.session_state.generated_story = result
                st.success("Story generated successfully!")
            else:
                st.session_state.generated_story = None
                st.error(result)

        # --- Display story from session state ---
        if st.session_state.generated_story:
            display_story(
                st.session_state.generated_story,
                st.session_state.generated_caption,
            )

    else:
        # Reset everything when image is removed.
        st.session_state.generated_story = None
        st.session_state.generated_caption = None
        st.info("👆 Upload an image above to get started!")


if __name__ == "__main__":
    main()