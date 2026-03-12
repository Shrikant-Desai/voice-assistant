import asyncio
import os
import pygame
import edge_tts
import speech_recognition as sr
from utils.logger import get_logger
from config import TTS_VOICE, TTS_OUTPUT_FILE

logger = get_logger(__name__)


class SpeechEngine:
    """Handles all speech input (STT) and output (TTS)."""

    def __init__(self):
        pygame.mixer.init()
        self.recognizer = sr.Recognizer()
        # Tune for ambient noise
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    # ── TTS ──────────────────────────────────────────────────────────────

    async def _synthesize(self, text: str) -> None:
        communicate = edge_tts.Communicate(text, TTS_VOICE)
        await communicate.save(TTS_OUTPUT_FILE)

        pygame.mixer.music.load(TTS_OUTPUT_FILE)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(TTS_OUTPUT_FILE)

    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        logger.info(f"Jarvis: {text}")
        asyncio.run(self._synthesize(text))

    # ── STT ──────────────────────────────────────────────────────────────

    def listen(self, prompt: str = "Listening...") -> str | None:
        """
        Listen from the microphone and return recognized text.
        Returns None if speech could not be understood.
        """
        logger.info(prompt)
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            text = self.recognizer.recognize_google(audio)
            logger.info(f"Heard: {text}")
            return text

        except sr.WaitTimeoutError:
            logger.warning("Listening timed out.")
        except sr.UnknownValueError:
            logger.warning("Could not understand audio.")
        except sr.RequestError as e:
            logger.error(f"STT API error: {e}")

        return None
