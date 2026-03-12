
# ============================================
# config.py — Application Configuration
# ============================================
# This module loads environment variables and
# defines settings used across the project.
# ============================================
import os
from dotenv import load_dotenv
# Load variables from .env file into the environment.
# This must be called BEFORE os.getenv() so the values are available.
load_dotenv()


# --- API Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# --- Story Categories ---
# These are the default categories shown in the UI dropdown.
# We define them here so they can be reused by any module.
STORY_CATEGORIES = [
    "Fantasy",
    "Horror",
    "Adventure",
    "Comedy",
    "Sci-Fi",
    "Romance",
    "Mystery",
]

# --- Image Settings ---
# Maximum file size in MB for uploaded images.
MAX_IMAGE_SIZE_MB = 5

# Supported image formats.
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]