from core.speech import SpeechEngine
from core.ai_engine import AIEngine
from skills.browser import try_open_browser
from skills.news import fetch_headlines
from config import WAKE_WORD
from utils.logger import get_logger

logger = get_logger(__name__)


class Assistant:
    """
    Main orchestrator: listens for the wake word,
    routes commands to the right skill or the AI engine.
    """

    def __init__(self):
        self.speech = SpeechEngine()
        self.ai = AIEngine()
        logger.info("Assistant initialized.")

    def _process_command(self, command: str) -> None:
        """Route a command to the appropriate skill or AI fallback."""

        # 1. Browser shortcuts
        if try_open_browser(command):
            return

        # 2. News
        if "news" in command.lower():
            headlines = fetch_headlines()
            if headlines:
                self.speech.speak(f"Here are the top {len(headlines)} headlines.")
                for headline in headlines:
                    self.speech.speak(headline)
            else:
                self.speech.speak("Sorry, I couldn't fetch the news right now.")
            return

        # 3. AI fallback
        answer = self.ai.ask(command)
        self.speech.speak(answer)

    def run(self) -> None:
        """Main loop: idle until wake word, then process one command."""
        self.speech.speak("Initializing Jarvis, your personal voice assistant.")

        while True:
            text = self.speech.listen("Waiting for wake word...")

            if text and WAKE_WORD in text.lower():
                self.speech.speak("Yes, what can I do for you?")
                command = self.speech.listen("Jarvis is active...")

                if command:
                    self._process_command(command)
                else:
                    self.speech.speak("I didn't catch that. Please try again.")
