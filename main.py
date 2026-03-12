import speech_recognition as sr
import asyncio
import edge_tts
import os
import pygame
import webbrowser
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")


newsapi = os.getenv("NEWS_API_KEY")

pygame.mixer.init()

# Initialize the Gemini API client
client = genai.Client(api_key=api_key)


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


def aiProcess(c):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents="You are voice assistant. You are helpful and precise. Answer the question in a concise manner.\n\n"
            + c,
            # config=types.GenerateContentConfig(
            #     thinking_config=types.ThinkingConfig(thinking_level="low")
            # ),
        )
        print("AI Response:", response.text)
        return response.text
    except Exception as e:
        print("Error generating content:", e)
        return "Sorry, I encountered an error while generating the response."


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            print(data)

            # Extract the articles
            articles = data.get("articles", [])

            # Print the headlines
            for article in articles:
                print(" >>>>>>> in the loop", article["title"])
                say(article["title"])

    else:

        output = aiProcess(c)
        say(output)


if __name__ == "__main__":
    say("Initializing Jarvis your personal voice assistant....")

    while True:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak something...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)

            if text.lower() == "jarvis":
                say("Yes, what can i do for you?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis is Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    print("Command>>>>>>>>", command)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("API unavailable")
