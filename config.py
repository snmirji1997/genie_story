# ============================================
# config.py — Application Configuration
# ============================================
# This module loads environment variables and
# defines settings used across the project.
# Supports both local (.env) and cloud (st.secrets) environments.
# ============================================

import os
import streamlit as st

# Try to load .env file for local development.
# If python-dotenv is not installed (e.g., on Streamlit Cloud),
# we skip it silently — the app will use st.secrets instead.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- API Configuration ---
# Try Streamlit Cloud secrets first, then fall back to .env file.
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")

# --- Story Categories ---
STORY_CATEGORIES = [
    "Fantasy",
    "Horror",
    "Adventure",
    "Comedy",
    "Sci-Fi",
    "Romance",
    "Mystery",
]

# --- Tone Options ---
STORY_TONES = [
    "Dramatic",
    "Lighthearted",
    "Dark",
    "Humorous",
    "Suspenseful",
    "Whimsical",
]

# --- Image Settings ---
MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]