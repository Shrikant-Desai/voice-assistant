import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Assistant settings
ASSISTANT_NAME = "jarvis"
WAKE_WORD = "jarvis"
TTS_VOICE = "en-US-AriaNeural"
TTS_OUTPUT_FILE = "speech.mp3"
GEMINI_MODEL = "gemini-2.5-flash-lite"

AI_SYSTEM_PROMPT = (
    "You are Jarvis, a voice assistant. "
    "Be helpful, concise, and conversational. "
    "Avoid markdown or bullet points — respond in plain spoken sentences only."
)

# News settings
NEWS_COUNTRY = "us"
NEWS_MAX_ARTICLES = 5

# URLs
BROWSER_SHORTCUTS = {
    "open google": "https://google.com",
    "open facebook": "https://facebook.com",
    "open youtube": "https://youtube.com",
    "open linkedin": "https://linkedin.com",
    "open github": "https://github.com",
}
