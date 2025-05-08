import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI

# APIt
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# Google-haun aikavälit
TBS_MAPPING = {
    "Tänään": "qdr:d",
    "Viime viikko": "qdr:w1",
    "Viime kuukausi": "qdr:m",
    "Viime vuosi": "qdr:y"
}

# Streamlit UI
st.set_page_config(page_title="Uutishaku ja Yhteenveto")
st.title("Uutishaku ja Yhteenveto")

with st.sidebar:
    st.subheader("🔍 Hakuvaihtoehdot")
    query = st.text_input("Anna hakusana tai aihe (esim. tekoäly, sähköauto)")
    time_range = st.selectbox("Aikaväli", list(TBS_MAPPING.keys()))
    num_results = st.slider("Tulosten määrä", 1, 10, 5)

if st.button("Hae uutiset ja tee yhteenveto") and query:
    with st.spinner("Haetaan uutisia..."):
        try:
            search = GoogleSerperAPIWrapper(
                type="news",
                params={"tbs": TBS_MAPPING[time_range]},
                serper_api_key=serper_api_key
            )
            results = search.results(query)
            news_items = results.get("news", [])[:num_results]

            if not news_items:
                st.warning("Uutisia ei löytynyt annetulla haulla.")
                st.stop()

            st.subheader("Uutiset")

            # LLM tiivistämiseen
            llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4", temperature=0.5)

            for i, item in enumerate(news_items, 1):
                st.markdown(f"**{i}. {item['title']}**")
                st.markdown(f"[Lue lisää]({item['link']})")
                st.markdown(f"> {item.get('snippet', '')}")

                # Luo lyhyt tiivistelmä uutisesta
                full_text = f"{item['title']}\n{item.get('snippet', '')}"
                prompt = f"Tiivistä seuraava uutinen yhdellä lyhyellä lauseella suomeksi:\n\n{full_text}"

                try:
                    summary = llm.predict(prompt)
                    st.info(f"Tiivistelmä: {summary}")
                except Exception as e:
                    st.warning(f"Tiivistelmä epäonnistui: {e}")

                st.markdown("---")

        except Exception as e:
            st.error(f"Tapahtui virhe: {e}")
