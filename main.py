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
        # Let OpenAI handle the request
        # output = aiProcess(c)
        # speak(output)
        say("Sorry, Veeram")


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

                    processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("API unavailable")
