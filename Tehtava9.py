

import google.generativeai as genai
import os
import sys

# Tarkistetaan käsky
if len(sys.argv) < 2:
    print("Käyttö: python Tehtava9.py kuva1.jpg kuva2.jpg ...")
    sys.exit(1)

# API-avain 
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))



# Kuvien lataus
image_files = []
for filename in sys.argv[1:]:
    try:
        uploaded = genai.upload_file(filename, display_name=f"Kuva: {filename}")
        image_files.append(uploaded)
        print(f"Ladattiin kuva: {filename}")
    except Exception as e:
        print(f"Virhe ladattaessa {filename}: {e}")

if not image_files:
    print("Yhtään kuvaa ei saatu ladattua, ohjelma keskeytetään.")
    sys.exit(1)

# Lisätiedot
user_input = input("Anna lisätietoa tuotteista (esim. kohderyhmä, käyttötarkoitus): ")

# Malli
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Prompt
prompt = [
    *image_files,
    f"Kirjoita jokaisesta kuvasta tuotekuvaus ja iskevä markkinointilause. "
    f"Ota huomioon seuraavat lisätiedot: {user_input}"
]


response = model.generate_content(prompt)

# Tulostus
print("\n--- LLM:n generoimat kuvaukset ja sloganit ---")
print(response.text)
