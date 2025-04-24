import sys
import os
import base64
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI()  #OPENAI_API_KEY

# Kuvatiedosto
image_path = sys.argv[1] if len(sys.argv) > 1 else "drawing1.png"

# Muunna kuva base64-muotoon
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

base64_image = encode_image(image_path)

# 1. Kuvan kuvaus (image → text)
vision_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in detail."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ],
        }
    ],
    max_tokens=500,
)

description = vision_response.choices[0].message.content
print("📝 Kuvaus kuvasta:\n")
print(description)

# Text to  image
image_response = client.images.generate(
    model="dall-e-3",
    prompt=description,
    n=1,
    size="1024x1024",
    response_format="b64_json",
)

# 3. Tallenna kuva
image_b64 = image_response.data[0].b64_json
image_data = base64.b64decode(image_b64)
image = Image.open(BytesIO(image_data))
image.save("generated_from_description.png")
print("\n✅ Uusi kuva tallennettu tiedostoon 'generated_from_description.png'")

