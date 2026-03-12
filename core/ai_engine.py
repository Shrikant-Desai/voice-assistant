from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL, AI_SYSTEM_PROMPT
from utils.logger import get_logger

logger = get_logger(__name__)


class AIEngine:
    """Wrapper around the Gemini generative AI client."""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def ask(self, user_input: str) -> str:
        """Send a prompt to Gemini and return the response text."""
        try:
            full_prompt = f"{AI_SYSTEM_PROMPT}\n\nUser: {user_input}"
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=full_prompt,
            )
            answer = response.text.strip()
            logger.debug(f"AI response: {answer}")
            return answer

        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return "Sorry, I ran into an error. Please try again."
