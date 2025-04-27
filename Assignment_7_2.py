# Prompt Create an interpreter program with Python code. The program records a user's voice. Recorded voice should be transcribed as a text output. Then the transcribed text into another language which is selected by the user. Available languages should be English, French and Finnish. User should be asked which language the user wants to text to be translated. Translated text should be able to speak out load. There should be also a calculation which calculates how many seconds translation from the original speech to user's selected language takes.
# Google Gemini 2.5 Pro (experimental)

import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import time
import os
import io

# --- Configuration ---
RECORDING_DURATION_SECONDS = 7 # How long to record audio
SAMPLE_RATE = 44100  # Sample rate for audio recording
RECORDING_FILENAME = "user_recording.wav"
TRANSLATED_AUDIO_FILENAME = "translated_output.mp3"

SUPPORTED_LANGUAGES = {
    "english": "en",
    "french": "fr",
    "finnish": "fi"
}

# --- Functions ---

def get_target_language():
    """Asks the user to select a target language and validates the input."""
    print("Please choose a target language for translation:")
    for lang_name in SUPPORTED_LANGUAGES:
        print(f"- {lang_name.capitalize()}")

    while True:
        choice = input("Enter your choice: ").lower().strip()
        if choice in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[choice], choice # Return code and full name
        else:
            print(f"Invalid choice. Please enter one of {', '.join(SUPPORTED_LANGUAGES.keys())}.")

def record_audio(filename, duration, fs):
    """Records audio from the default microphone."""
    print(f"\nRecording for {duration} seconds... Please speak clearly.")
    try:
        # Record audio
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        # Save as WAV file
        write(filename, fs, recording)
        print(f"Recording saved as {filename}")
        return True
    except Exception as e:
        print(f"Error during recording: {e}")
        return False

def transcribe_audio(filename):
    """Transcribes audio from a WAV file using Google Web Speech API."""
    print("Transcribing audio...")
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            print(f"Transcription successful: '{text}'")
            return text
    except sr.UnknownValueError:
        print("Transcription failed: Google Speech Recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Transcription failed: Could not request results from Google Speech Recognition service; {e}")
        return None
    except FileNotFoundError:
        print(f"Transcription failed: Audio file {filename} not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during transcription: {e}")
        return None


def translate_text(text, target_lang_code):
    """Translates text to the target language."""
    print(f"Translating text to language code: '{target_lang_code}'...")
    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang_code).translate(text)
        print(f"Translation successful: '{translated_text}'")
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def speak_text(text, lang_code, output_filename):
    """Converts text to speech and plays it."""
    print("Generating spoken audio...")
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(output_filename)
        print(f"Translated audio saved as {output_filename}")
        print("Speaking translated text...")
        playsound(output_filename)
        return True
    except Exception as e:
        print(f"Error during text-to-speech or playback: {e}")
        return False

def cleanup_files(*filenames):
    """Removes specified temporary files."""
    for filename in filenames:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                # print(f"Cleaned up {filename}") # Optional: uncomment for verbose cleanup
        except Exception as e:
            print(f"Warning: Could not clean up file {filename}: {e}")

# --- Main Program ---
if __name__ == "__main__":
    start_time = time.perf_counter() # Start the timer

    # 1. Get target language from user
    target_lang_code, target_lang_name = get_target_language()
    print(f"Target language set to: {target_lang_name.capitalize()} ({target_lang_code})")

    # 2. Record Audio
    if not record_audio(RECORDING_FILENAME, RECORDING_DURATION_SECONDS, SAMPLE_RATE):
        print("Exiting due to recording error.")
        exit()

    # 3. Transcribe Audio
    original_text = transcribe_audio(RECORDING_FILENAME)

    translated_text = None
    if original_text:
        # 4. Translate Text
        translated_text = translate_text(original_text, target_lang_code)

    speech_successful = False
    if translated_text:
        # 5. Speak Translated Text
        speech_successful = speak_text(translated_text, target_lang_code, TRANSLATED_AUDIO_FILENAME)

    # 6. Calculate and display time
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"\n--------------------------------------------------")
    print(f"Process completed.")
    if original_text:
        print(f"Original Text: '{original_text}'")
    if translated_text:
        print(f"Translated Text ({target_lang_name.capitalize()}): '{translated_text}'")
    if speech_successful:
        print(f"Translated text was spoken successfully.")
    else:
         print(f"Translated text could not be spoken.")

    print(f"Total time taken: {elapsed_time:.2f} seconds")
    print(f"--------------------------------------------------")


    # 7. Cleanup temporary files
    cleanup_files(RECORDING_FILENAME, TRANSLATED_AUDIO_FILENAME)