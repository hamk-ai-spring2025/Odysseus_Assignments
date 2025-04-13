import os
from dotenv import load_dotenv
from openai import OpenAI
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import time

# API-avain
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Nauhoita puhe 
def nauhoita_puhe(filename="user_input.wav", duration=4, fs=44100):
    print("Puhu nyt mikrofoniin...")
    tallenne = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Nauhoitus valmis.")
    write(filename, fs, tallenne)
    return filename

# Whisper STT
def tunnista_puhe(file_path):
    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="fi"
        )
    return transcription.text

# GPT-vitsi
def generoi_vitsi(aihe):
    promptti = f"Kerro hauska vitsi aiheesta: {aihe}"
    vastaus = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": promptti}],
        temperature=0.8,
        max_tokens=60
    )
    return vastaus.choices[0].message.content.strip()

# OpenAI TTS
def puhu_openai_tts(teksti, voice="nova"):
    print("Luodaan ääni OpenAI TTS:llä...")
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=teksti
    )
    temp_path = os.path.join(tempfile.gettempdir(), f"vitsi_{int(time.time())}.mp3")
    with open(temp_path, "wb") as f:
        f.write(response.content)
    print("▶️ Toistetaan vitsi...")
    os.system(f'start {temp_path}')  

# Ohjelma
def main():
    audiotiedosto = "user_input.wav"
    nauhoita_puhe(audiotiedosto)
    aihe = tunnista_puhe(audiotiedosto)
    print("Tunnistettu aihe:", aihe)

    vitsi = generoi_vitsi(aihe)
    print("GPT-vitsi:", vitsi)

    puhu_openai_tts(vitsi, voice="nova")  # Ääntä voi vaihtaa

if __name__ == "__main__":
    main()

