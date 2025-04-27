# Prompt Create a voice controlled program with Python code. The program should utilize OpenAI API. The user has OpenAI API Key as a variable on the computer. The program uses voice input and generates images.
# ChatGPT

import os
import speech_recognition as sr
import openai
import requests
from PIL import Image
from io import BytesIO

# Fetch the OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❗ OPENAI_API_KEY environment variable not found.")

def record_voice():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("🎤 Speak your image idea...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

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
        size="512x512"  # Can also be "1024x1024"
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