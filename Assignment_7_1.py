# Prompt Create an interpreter program with Python code. The program records a user's voice. Recorded voice should be transcribed as a text output. Then the transcribed text into another language which is selected by the user. Available languages should be English, French and Finnish. User should be asked which language the user wants to text to be translated. Translated text should be able to speak out load. There should be also a calculation which calculates how many seconds translation from the original speech to user's selected language takes.
# Google Gemini 2.5 Flash (experimental)

import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import time
import tempfile
import sys # Import sys to check platform

# Configuration
fs = 44100  # Sample rate
duration = 5 # seconds per recording segment

# Create a temporary file for recording
# Using tempfile ensures a unique name and handles cleanup robustly
temp_audio_file = None
try:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
         temp_audio_file = fp.name
except Exception as e:
    print(f"Error creating temporary file: {e}")
    sys.exit("Cannot proceed without a temporary file.")


# Language mapping for user input, googletrans, and gtts
LANGUAGES = {
    "english": {"code": "en", "gtts_code": "en"},
    "french": {"code": "fr", "gtts_code": "fr"},
    "finnish": {"code": "fi", "gtts_code": "fi"}
}

def record_audio(filename, seconds, sample_rate):
    """Records audio from the microphone."""
    print("\nPress Enter to start speaking. Recording will last for", seconds, "seconds after you press Enter.")
    input() # Wait for user to press Enter
    print("Recording...")
    try:
        # Use sounddevice to record
        recording = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        sf.write(filename, recording, sample_rate) # Use soundfile
        print(f"Recording finished.")
        return True
    except Exception as e:
        print(f"Error during recording: {e}")
        print("Please ensure you have a working microphone and necessary dependencies (like PortAudio for sounddevice).")
        return False

def transcribe_audio(audio_file):
    """Transcribes audio using Google Web Speech API."""
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)  # read the entire audio file
    except Exception as e:
        print(f"Error reading audio file {audio_file}: {e}")
        return None


    text = None
    try:
        print("Transcribing...")
        # Use Google Web Speech API
        text = r.recognize_google(audio)
        print(f"Transcription: {text}")
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio (Speech is unintelligible)")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API service; {e}")
        print("Please check your internet connection.")
    except Exception as e:
        print(f"An unexpected error occurred during transcription: {e}")
    return text

def translate_text(text, target_language_code):
    """Translates text using deep-translator."""
    translated_text = None
    try:
        print(f"Translating to {target_language_code}...")
        # Use deep_translator: source='auto' detects source language
        translated_text = GoogleTranslator(source='auto', target=target_language_code).translate(text)
        if translated_text: # Check if translation returned something
             print(f"Translation: {translated_text}")
        else:
             print("Translation returned an empty result.")
    except Exception as e:
        print(f"Error during translation: {e}")
        print("Translation service might be temporarily unavailable or input is invalid.")
    return translated_text

def speak_text(text, lang_gtts_code):
    """Speaks text aloud using gTTS and plays it."""
    try:
        tts = gTTS(text=text, lang=lang_gtts_code, slow=False)
        # Save to a temporary file and play
        # Use tempfile for a safer temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
             temp_mp3_file = fp.name
        tts.save(temp_mp3_file)

        print("Speaking translation...")
        # Attempt to play the file using playsound or system commands
        try:
            import playsound
            # playsound might have issues with certain paths or environments
            # Use the absolute path just in case
            playsound.playsound(os.path.abspath(temp_mp3_file))
        except ImportError:
            print("playsound library not found. Install it (`pip install playsound`).")
            print("Attempting to play using system default (less reliable)...")
            # Fallback to system commands if playsound is not available
            try:
                if sys.platform.startswith('win'): # Windows
                    os.system(f"start {temp_mp3_file}")
                elif sys.platform.startswith('darwin'): # macOS
                    os.system(f"afplay {temp_mp3_file}")
                else: # Linux/other (requires mpg123 or similar command-line player)
                    os.system(f"mpg123 {temp_mp3_file}") # requires mpg123 installed
            except Exception as e:
                print(f"Could not play audio using system command: {e}")
                print("Please ensure you have a compatible audio player installed and in your system's PATH.")

        # Clean up the temporary file
        # Give it a moment before trying to delete, especially on Windows
        time.sleep(1) # Small delay
        if os.path.exists(temp_mp3_file):
            try:
                os.remove(temp_mp3_file)
            except Exception as e:
                 print(f"Could not remove temporary audio file {temp_mp3_file}: {e}")


    except Exception as e:
        print(f"Error during text-to-speech: {e}")
        print("Please check your internet connection and ensure gTTS can generate speech for the selected language.")


def get_target_language():
    """Gets valid target language input from the user."""
    print("\nAvailable languages for translation:")
    for name in LANGUAGES:
        print(f"- {name.capitalize()} ({LANGUAGES[name]['code']})")

    while True:
        user_input = input("Enter the target language name or code (e.g., French or fr): ").strip().lower()
        for name, codes in LANGUAGES.items():
            if user_input == name or user_input == codes['code']:
                return codes['code'] # Return the code for googletrans and finding gtts code
        print("Invalid language name or code. Please try again.")

# Main program execution
if __name__ == "__main__":
    print("--- Voice Interpreter ---")
    print("This program records your voice, transcribes it, translates it, and speaks the translation.")
    print("Recording duration is set to", duration, "seconds per turn.")

    target_lang_code = get_target_language()
    # Find the gtts code for the selected language
    target_gtts_code = None
    for lang_info in LANGUAGES.values():
        if lang_info['code'] == target_lang_code:
            target_gtts_code = lang_info['gtts_code']
            break

    if not target_gtts_code:
         print("Internal error: Could not find gTTS code for selected language.")
         sys.exit()


    try:
        while True:
            # 1. Record audio
            if record_audio(temp_audio_file, duration, fs):
                # 2. Transcribe audio
                transcribed_text = transcribe_audio(temp_audio_file)

                if transcribed_text:
                    # 3. Translate text and measure time
                    start_time = time.time()
                    translated_text = translate_text(transcribed_text, target_lang_code)
                    end_time = time.time()
                    translation_duration = end_time - start_time

                    if translated_text:
                        # 4. Report translation time
                        print(f"\nTranslation took: {translation_duration:.2f} seconds")
                        # 5. Speak translated text
                        speak_text(translated_text, target_gtts_code)
                    else:
                        print("Translation failed.")
                else:
                    print("Transcription failed. Cannot proceed with translation and speech.")

            # Ask user to continue
            while True:
                continue_input = input("\nInterpret another phrase? (yes/no): ").strip().lower()
                if continue_input in ['yes', 'y']:
                    break # Exit this inner loop to continue
                elif continue_input in ['no', 'n']:
                    print("Exiting interpreter. Goodbye!")
                    sys.exit() # Exit the program
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

    except KeyboardInterrupt:
        print("\nInterpreter stopped by user.")
    finally:
        # Clean up the temporary audio file if it still exists
        if temp_audio_file and os.path.exists(temp_audio_file):
            try:
                os.remove(temp_audio_file)
                print(f"Cleaned up temporary file: {temp_audio_file}")
            except Exception as e:
                 print(f"Could not remove temporary file {temp_audio_file} during cleanup: {e}")