import time
import sounddevice as sd
import soundfile as sf
import tempfile
import whisper
from openai import OpenAI
from gtts import gTTS
import pygame

# OpenAI
client = OpenAI()

# Asetukset
DURATION = 5  # puheen tallennuksen kesto sekunteina
LANGUAGE_FROM = "fi"  # Whisper kieli
LANGUAGE_TO = "German"  # GPT-käännös kieli
TTS_LANG_CODE = "de"  # de = saksa

# Nauhoitus
fs = 44100
print(" Nauhoitetaan puhetta...")
start_time = time.time()
recording = sd.rec(int(DURATION * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()
print(" Nauhoitus valmis.")

# TTallennus WAV
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
    wav_file = tmpfile.name
    sf.write(wav_file, recording, fs)

#  Whisper
print(" Tunnistetaan puhe Whisperillä...")
model = whisper.load_model("base")
result = model.transcribe(wav_file, language=LANGUAGE_FROM)
original_text = result["text"]
print("Tunnistettu suomenkielinen teksti:", original_text)

#  Käännös kohdekielelle
def translate_with_gpt(text, target_language="German"):
    prompt = f"Translate the following Finnish text to {target_language}:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

print(f"Käännetään suomesta → {LANGUAGE_TO}...")
translated_text = translate_with_gpt(original_text, target_language=LANGUAGE_TO)
print(f" Käännös ({LANGUAGE_TO}):", translated_text)

#  Teksti puheeksi gTTS:llä
print(" Luodaan puhe...")
tts = gTTS(translated_text, lang=TTS_LANG_CODE)
tts_file = "output.mp3"
tts.save(tts_file)

#  Toistetaan pygame:llä
print(" Toistetaan...")
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(tts_file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# Viive
end_time = time.time()
print(f"⏱Kokonaisviive: {end_time - start_time:.2f} sekuntia")


