# Prompt Improve the previous Python code that recording time is 10 seconds. The recoding time is shown to the user.
# ChatGPT

import os
import time
import threading
import speech_recognition as sr
import openai
import requests
from PIL import Image
from io import BytesIO

# Fetch the OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❗ OPENAI_API_KEY environment variable not found.")

RECORD_SECONDS = 10  # How long to record

def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"⏳ Recording... {remaining} seconds remaining", end='\r')
        time.sleep(1)
    print("\n🎤 Recording finished.\n")

def record_voice(duration=RECORD_SECONDS):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print(f"🎙️ Starting to record for {duration} seconds...")
        recognizer.adjust_for_ambient_noise(source)

        # Start the countdown in a separate thread
        countdown_thread = threading.Thread(target=countdown_timer, args=(duration,))
        countdown_thread.start()

        audio = recognizer.record(source, duration=duration)

        countdown_thread.join()

    try:
        print("🧠 Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❗ Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"❗ API request error: {e}")
        return None

def generate_image(prompt):
    print("🎨 Generating image from your prompt...")
    response = openai.images.generate(
        prompt=prompt,
        n=1,
        size="512x512"  # You can also use "1024x1024" for bigger images
    )
    image_url = response.data[0].url
    print(f"🖼️ Image URL: {image_url}")
    return image_url

def download_and_show_image(url):
    print("⬇️ Downloading image...")
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.show()

def main():
    input("Press Enter to start recording your image prompt...")
    prompt = record_voice()
    if not prompt:
        return

    image_url = generate_image(prompt)
    download_and_show_image(image_url)

if __name__ == "__main__":
    main()
