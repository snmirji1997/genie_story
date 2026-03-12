# ============================================
# app.py — Genie Image Story Generator (Main)
# ============================================
# This is the Streamlit UI that ties together
# config, prompts, and gemini_service modules.
# ============================================

import io
import streamlit as st
from PIL import Image

from config import GEMINI_API_KEY, STORY_CATEGORIES, MAX_IMAGE_SIZE_MB, ALLOWED_IMAGE_TYPES
from prompts import build_story_prompt
from gemini_service import generate_story


# --- Page Configuration ---
# Must be the FIRST Streamlit command in the script.
# Sets the browser tab title, icon, and page layout.
st.set_page_config(
    page_title="Genie Image Story Generator",
    page_icon="🧞",
    layout="centered",
)


def validate_image(uploaded_file):
    """
    Validate the uploaded image file.

    Checks:
        1. File size is within the allowed limit.
        2. File type is in the allowed formats.

    Args:
        uploaded_file: The file object from st.file_uploader.

    Returns:
        tuple: (is_valid: bool, message: str)
    """

    # Check file size.
    # uploaded_file.size gives bytes, so we convert MB to bytes.
    max_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
    if uploaded_file.size > max_bytes:
        return (False, f"Image too large. Maximum size is {MAX_IMAGE_SIZE_MB}MB.")

    # Check file type.
    # uploaded_file.type gives something like "image/jpeg".
    # We extract the part after "/" and compare with our allowed list.
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
        tuple: (category: str, length: str, instructions: str)
    """

    with st.sidebar:
        st.header("⚙️ Story Settings")

        # --- Category Selection ---
        category = st.selectbox(
            "Choose a genre:",
            options=STORY_CATEGORIES,
            index=0,  # Default to first item ("Fantasy")
        )

        # --- Story Length ---
        length = st.selectbox(
            "Story length:",
            options=["Short", "Medium", "Long"],
            index=1,  # Default to "Medium"
        )

        # --- Extra Instructions ---
        instructions = st.text_area(
            "Additional instructions (optional):",
            placeholder="e.g., Include a talking cat, set it in ancient Egypt...",
            height=120,
        )

        st.divider()
        st.markdown("Built with 🧞 Gemini + Streamlit")

    return category, length, instructions


def main():
    """Main application flow."""

    # --- Step 1: Check API Key ---
    # If the key is missing, show a warning and stop.
    if not GEMINI_API_KEY:
        st.error("⚠️ Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
        st.stop()

    # --- Step 2: Display header and sidebar ---
    display_header()
    category, length, instructions = display_sidebar()

    # --- Step 3: Image Upload ---
    uploaded_file = st.file_uploader(
        "Upload an image to inspire your story:",
        type=ALLOWED_IMAGE_TYPES,
        help=f"Max size: {MAX_IMAGE_SIZE_MB}MB. Formats: {', '.join(ALLOWED_IMAGE_TYPES)}",
    )

    # --- Step 4: Process the uploaded image ---
    if uploaded_file is not None:

        # Validate the image.
        is_valid, message = validate_image(uploaded_file)
        if not is_valid:
            st.error(message)
            st.stop()

        # Open the image using Pillow.
        # BytesIO wraps the raw bytes so Pillow can read them like a file.
        image = Image.open(io.BytesIO(uploaded_file.read()))

        # Display the uploaded image in the UI.
        st.image(image, caption="Your uploaded image", use_container_width=True)

        # --- Step 5: Generate Story Button ---
        if st.button("🧞 Generate Story", type="primary", use_container_width=True):

            # Build the prompt using our prompts module.
            prompt = build_story_prompt(category, instructions, length)

            # Call Gemini with a loading spinner.
            with st.spinner("🧞 The Genie is crafting your story..."):
                success, result = generate_story(image, prompt)

            # --- Step 6: Display Results ---
            if success:
                st.success("Story generated successfully!")
                st.divider()
                st.markdown(result)
            else:
                st.error(result)

    else:
        # Show a helpful message when no image is uploaded yet.
        st.info("👆 Upload an image above to get started!")


# --- Entry Point ---
# Streamlit runs the script top-to-bottom, but wrapping logic
# in main() keeps the code organized and testable.
if __name__ == "__main__":
    main()