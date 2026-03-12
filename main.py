import speech_recognition as sr
import asyncio
import edge_tts
import os
import pygame
import webbrowser
import requests


newsapi = "462584cebcad459ebe2287eff081e9bb"

pygame.mixer.init()


async def speak(text):
    filename = "speech.mp3"

    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("speech.mp3")


def say(text):
    asyncio.run(speak(text))


if __name__ == "__main__":
    say("Initializing your personal voice assistant....")

    while True:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak something...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)

            if text.lower() == "hey buddy":
                say("Yes, I am here. tell me what can i do for you?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Buddy is Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    print(">>>>>>>>", command)

                    # processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("API unavailable")
