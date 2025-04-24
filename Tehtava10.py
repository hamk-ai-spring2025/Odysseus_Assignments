
import google.generativeai as genai
import os

# API-avain 
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Kysy sana
word = input("Anna sana: ").strip()

# Prompt
prompt = (
    f"Anna sanakirjamainen vastaus sanalle '{word}' seuraavassa JSON-muodossa:\n"
    "{\n"
    "  \"word\": \"...\",\n"
    "  \"definitions\": [\"...\"],\n"
    "  \"synonyms\": [\"...\"],\n"
    "  \"antonyms\": [\"...\"],\n"
    "  \"examples\": [\"...\"]\n"
    "}\n"
    "Palauta ainoastaan kelvollinen JSON ilman mitään muuta tekstiä."
)

# LLM-malli
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Vastaus
response = model.generate_content(prompt)

# Tulostetaan JSON
print(response.text.strip())
