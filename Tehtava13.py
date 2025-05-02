import streamlit as st
import replicate
import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO

# API-avain 
load_dotenv()
replicate_token = os.getenv("REPLICATE_API_TOKEN") 

# UI
st.title("Image Generator")


prompt = st.text_area("Prompt", placeholder="for example: fancy car")
neg_prompt = st.text_area("Negative prompt", placeholder="for example: red car")
aspect = st.selectbox("Aspect ratio", ["1:1", "16:9", "3:2", "9:16", "4:5"])
aspect_map = {
    "1:1": [512, 512],
    "16:9": [768, 432],
    "3:2": [768, 512],
    "9:16": [432, 768],
    "4:5": [512, 640]
}

if st.button("Generate Image") and prompt and replicate_token:
    st.info("Generating image...")

    width, height = aspect_map[aspect]

    client = replicate.Client(api_token=replicate_token)

    try:
        output = client.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={
                "prompt": prompt,
                "negative_prompt": neg_prompt,
                "width": width,
                "height": height,
                "scheduler": "K_EULER"
            }
        )

        for index, image_url in enumerate(output):
            img_data = requests.get(image_url).content
            img = Image.open(BytesIO(img_data))
            st.image(img, caption="Generated Image", use_container_width=True)

            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            st.download_button("Download Image", data=img_bytes.getvalue(), file_name="generated.png", mime="image/png")

    except Exception as e:
        st.error(f"Image generation failed: {str(e)}")
