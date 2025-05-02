import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

# Lataa .env-tiedosto
load_dotenv()

# Avaimet
openai_api_key = os.getenv("OPENAI_API_KEY") 
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") 

# GPT-4o
openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# UI
st.title("GPT-4o & Claude 3.5 ")

# Valinta
model_choice = st.radio("Valitse malli(t)", ["GPT-4o", "Claude 3.5 Sonnet", "Molemmat"], horizontal=True)

# Käyttäjä
user_input = st.text_input("Viestisi:")

if st.button("Lähetä"):
    if user_input:
        if model_choice == "GPT-4o" and openai_api_key:
            st.subheader("GPT-4o")
            try:
                gpt_response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": user_input}]
                )
                st.write(gpt_response.choices[0].message.content)
            except Exception as e:
                st.error(f"GPT-4o error: {str(e)}")

        elif model_choice == "Claude 3.5 Sonnet" and anthropic_api_key:
            st.subheader("Claude 3.5 Sonnet")
            try:
                headers = {
                    "x-api-key": anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "claude-3-5-sonnet-20240620",
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": user_input}]
                }
                response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
                reply = response.json()["content"][0]["text"]
                st.write(reply)
            except Exception as e:
                st.error(f"Claude error: {str(e)}")

        elif model_choice == "Molemmat":
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("GPT-4o")
                try:
                    gpt_response = openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": user_input}]
                    )
                    st.write(gpt_response.choices[0].message.content)
                except Exception as e:
                    st.error(f"GPT-4o error: {str(e)}")

            with col2:
                st.subheader("Claude 3.5 Sonnet")
                try:
                    headers = {
                        "x-api-key": anthropic_api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": "claude-3-5-sonnet-20240620",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": user_input}]
                    }
                    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
                    reply = response.json()["content"][0]["text"]
                    st.write(reply)
                except Exception as e:
                    st.error(f"Claude error: {str(e)}")
    else:
        st.warning("Anna viestisi, ennen lähetä-painikkeen painamista.")
