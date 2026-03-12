# ============================================
# config.py — Application Configuration
# ============================================
# This module loads environment variables and
# defines settings used across the project.
# Supports both local (.env) and cloud (st.secrets) environments.
# ============================================

import os
import streamlit as st
from dotenv import load_dotenv

# Load variables from .env file (used for local development).
load_dotenv()

# --- API Configuration ---
# Try Streamlit Cloud secrets first, then fall back to .env file.
# st.secrets is available when deployed on Streamlit Community Cloud.
# os.getenv reads from the .env file for local development.
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