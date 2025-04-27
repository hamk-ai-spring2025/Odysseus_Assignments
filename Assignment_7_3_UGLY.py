# Prompt Create an interpreter program with Python code. The program records a user's voice. Recorded voice should be transcribed as a text output. Then the transcribed text into another language which is selected by the user. Available languages should be English, French and Finnish. User should be asked which language the user wants to text to be translated. Translated text should be able to speak out load. There should be also a calculation which calculates how many seconds translation from the original speech to user's selected language takes.
# ChatGPT

import speech_recognition as sr
import time
from deep_translator import GoogleTranslator
import pyttsx3

# Initialize translator and speech engine
# translator = Translator()
engine = pyttsx3.init()

# Language codes for Google Translate
language_codes = {
    "english": "en",
    "french": "fr",
    "finnish": "fi"
}

def record_voice():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("🧠 Transcribing...")
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❗ Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"❗ Error with the speech recognition service: {e}")
        return None

def translate_text(text, target_language):
    print(f"🌎 Translating to {target_language.capitalize()}...")
    try:
        # Initialize translator here, specify source='auto'
        translator = GoogleTranslator(source='auto', target=language_codes[target_language.lower()])
        translated_text = translator.translate(text) # Simple call
        if translated_text:
             print(f"🔤 Translated Text: {translated_text}")
             return translated_text
        else:
             print("❗ Translation returned empty result.")
             return None
    except Exception as e:
        print(f"❗ Error during translation: {e}")
        return None

def speak_text(text):
    print("🔊 Speaking out loud...")
    engine.say(text)
    engine.runAndWait()

def main():
    # Step 1: Record and transcribe
    input("Press Enter to start recording...")
    start_time = time.time()
    original_text = record_voice()
    if not original_text:
        return

    # Step 2: Ask for translation language
    print("\nWhich language do you want to translate to?")
    print("Options: English, French, Finnish")
    target_language = input("Enter your choice: ").strip().lower()

    if target_language not in language_codes:
        print("❗ Invalid language selection.")
        return

    # Step 3: Translate
    translated_text = translate_text(original_text, target_language)

    # Step 4: Speak out the translated text
    speak_text(translated_text)

    # Step 5: Calculate time taken
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n⏱️ Translation process took {duration:.2f} seconds.")

if __name__ == "__main__":
    main()