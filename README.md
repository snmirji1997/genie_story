# 🧞 Genie Image Story Generator

An AI-powered Python application that generates creative stories from images using Google's Gemini Vision model.

Upload any image, choose a genre and tone, and watch as AI crafts a unique story inspired by what it sees.

---

## Features

- **Image Upload** — Supports JPG, JPEG, PNG, and WebP formats (up to 5MB)
- **7 Story Genres** — Fantasy, Horror, Adventure, Comedy, Sci-Fi, Romance, Mystery
- **Custom Genre** — Type any genre you can imagine (e.g., "Steampunk Western")
- **6 Tone Options** — Dramatic, Lighthearted, Dark, Humorous, Suspenseful, Whimsical
- **Story Length Control** — Short (150-250 words), Medium (400-600), or Long (800-1200)
- **AI Image Captioning** — Optional two-step pipeline where Gemini describes the image first, then uses that description to write a richer story
- **Story Download** — Save generated stories as .txt files
- **Extra Instructions** — Guide the AI with custom directions (e.g., "Include a talking cat")

---

## Tech Stack

| Library | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **Streamlit** | Web UI framework |
| **google-genai** | Google Gemini API SDK |
| **Pillow** | Image processing and validation |
| **python-dotenv** | Environment variable management |

---

## Project Structure

```
genie_story/
├── app.py               # Main Streamlit UI and application flow
├── gemini_service.py     # Gemini API integration (caption + story)
├── prompts.py            # Prompt templates and engineering
├── config.py             # Configuration and environment variables
├── requirements.txt      # Python dependencies
├── .env                  # API key (not committed to Git)
├── .gitignore            # Files excluded from version control
└── README.md             # This file
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd genie_story
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Gemini API key

1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### 5. Create a `.env` file

```bash
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual key. No quotes, no spaces around `=`.

---

## Usage

### Run the app

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

### How it works

1. Upload an image using the file uploader
2. Choose a genre from the sidebar (or select "Custom" to type your own)
3. Pick a tone and story length
4. Optionally add extra instructions
5. Click **🧞 Generate Story**
6. Read your story and download it as a .txt file

### AI Pipeline

When "Generate image caption first" is enabled (default):

```
Image → [Gemini: Caption] → Image Description → [Gemini: Story] → Final Story
```

The captioning step produces a detailed description of the image, which gets injected into the story prompt. This two-step approach gives the model richer context and produces higher quality stories.

---

## Configuration

All settings are centralized in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `STORY_CATEGORIES` | 7 genres | Predefined genre options |
| `STORY_TONES` | 6 tones | Writing style options |
| `MAX_IMAGE_SIZE_MB` | 5 | Maximum upload size in MB |
| `ALLOWED_IMAGE_TYPES` | jpg, jpeg, png, webp | Accepted image formats |

---

## Prompt Engineering

The prompt system in `prompts.py` uses several techniques:

- **Role Assignment** — "You are a master storyteller and creative writer"
- **Descriptor Expansion** — Tones are expanded into rich descriptions (e.g., "Dark" becomes "gritty, atmospheric, and unsettling with an ominous mood")
- **Concrete Constraints** — Word counts instead of vague terms like "short"
- **Structured Sections** — TASK, GENRE, TONE, RULES, and ADDITIONAL INSTRUCTIONS are clearly separated
- **Caption Injection** — AI-generated image description is included as context when available

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Activate the virtual environment: `source venv/bin/activate` |
| "API key not found" | Check your `.env` file exists and has the key set correctly |
| 429 Rate Limit Error | Wait a few minutes or switch model in `gemini_service.py` |
| "Content blocked" | Try a different image — some content triggers safety filters |
| App won't load | Make sure you're running from the `genie_story/` directory |

---

## Model

This project uses **Gemini 2.5 Flash** (`gemini-2.5-flash`), a multimodal model that understands both text and images. The model can be changed by updating `MODEL_NAME` in `gemini_service.py`.

---

## License

This project is for educational purposes. Built as a learning project for Python and GenAI development.