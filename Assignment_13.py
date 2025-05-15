#prompt Generate a code for a modern-style web interface as a Python code where an user can create an image using the Stable Diffusion AI image generator API. The user should have possibilities to define both a prompt and also a negative prompt. User should also have a possibility to define a ratio of the image. There should be a button where the user can download the created image. The code should use a real Stable Diffusion API. The Stable Diffusion API Key should be asked from the user on the web interface. The API key should not be hard coded in the code. The Python code should be supported to be run on Streamlit.

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(page_title="AI Image Generator", layout="centered")

st.title("🎨 AI Image Generator with Stable Diffusion")
st.markdown("Generate images using prompts and control the style with negative prompts. Choose your desired aspect ratio and download your result.")

# User inputs
api_key = st.text_input("🔐 Enter your Stability.ai API Key", type="password")
prompt = st.text_area("📝 Prompt", "A futuristic city at sunset, ultra-realistic")
negative_prompt = st.text_area("🚫 Negative Prompt", "blurry, low quality, dark")

aspect_ratio = st.selectbox(
    "📐 Select Aspect Ratio",
    ("1:1 (Square)", "16:9 (Widescreen)", "9:16 (Portrait)", "4:3", "3:2")
)

aspect_ratio_map = {
    "1:1 (Square)": (512, 512),
    "16:9 (Widescreen)": (896, 512),
    "9:16 (Portrait)": (512, 896),
    "4:3": (768, 576),
    "3:2": (768, 512),
}

width, height = aspect_ratio_map[aspect_ratio]

generate_button = st.button("🎨 Generate Image")

if generate_button:
    if not api_key:
        st.error("Please enter your Stability.ai API key.")
    else:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "output_format": "png",
            "seed": 0,
            "steps": 30,
            "cfg_scale": 7,
            "width": width,
            "height": height
        }

        with st.spinner("Generating image..."):
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/generate",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                image_bytes = base64.b64decode(response.json()["image"])
                image = Image.open(BytesIO(image_bytes))

                st.image(image, caption="Generated Image", use_column_width=True)

                # Download button
                download_btn = st.download_button(
                    label="💾 Download Image",
                    data=image_bytes,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            else:
                st.error("❌ Failed to generate image.")
                try:
                    st.json(response.json())
                except Exception:
                    st.text(response.text)
