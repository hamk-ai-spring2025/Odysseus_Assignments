import os
import json
import asyncio
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from langchain_openai import ChatOpenAI
from playwright.async_api import async_playwright

# Lataa API-avaimet .env-tiedostosta
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Scrapaa tuotetiedot verkkosivulta
async def scrape_product_data(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state('domcontentloaded')
        content = await page.content()
        await browser.close()

        soup = BeautifulSoup(content, "html.parser")

        # Alibaba-sivulle esimerkki: hae nimi, kuvaus, hinta (kokeile ja säädä tarvittaessa)
        name = soup.find("h1")
        desc = soup.find("meta", {"name": "description"})
        price = soup.find("span", class_="price") or soup.find("span", class_="Price--priceText")

        return {
            "product_name": name.get_text(strip=True) if name else "Unknown",
            "original_description": desc["content"] if desc and desc.get("content") else "No description available.",
            "price": price.get_text(strip=True) if price else "$39.99",
            "review_rating": "4.2"  # Scrapaus tähän mahdollista jos löytyy
        }

# Luo paranneltu kuvaus LangChainin avulla
def enhance_description(product_data):
    prompt_template = PromptTemplate.from_template("""
Tuotekuvaus: {description}
Hinta: {price}
Arvostelujen keskiarvo: {rating}

Kirjoita uusi houkutteleva tuotekuvaus, joka ottaa huomioon hinnan ja arvioinnin. Korosta tuotteen vahvuuksia, mutta ole realistinen.
""")
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.7, model="gpt-4")
    chain = (
        RunnableMap({
            "description": lambda x: x["original_description"],
            "price": lambda x: x["price"],
            "rating": lambda x: x["review_rating"]
        })
        | prompt_template
        | llm
        | StrOutputParser()
    )
    return chain.invoke(product_data)

# Pääohjelma
def main():
    url = input("Anna tuotteen URL-osoite: ")
    product_data = asyncio.run(scrape_product_data(url))
    product_data["enhanced_description"] = enhance_description(product_data)

    print(json.dumps(product_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

