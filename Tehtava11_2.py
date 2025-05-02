import os
import pypandoc
import anthropic

aihe = "Tekoälyn käyttö yläkoulussa: mahdollisuudet ja haasteet"

# API-avain
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

# Claude
viesti = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=2000,
    system=("Vastaa vain Markdown-muodossa. Kirjoita tieteellinen artikkeli suomeksi, "
            "jossa on Tiivistelmä, Johdanto, Luvut, Alaluvut, Johtopäätös ja APA-viitteet. "
            "Lisää yksi taulukko, jos mahdollista."),
    messages=[
        {
            "role": "user",
            "content": f"Kirjoita tieteellinen artikkeli aiheesta '{aihe}'. Käytä APA-viitteitä ja Markdown-muotoilua."
        }
    ]
)

markdown_teksti = viesti.content[0].text

# Tallennetaan Markdown väliaikaiseen tiedostoon
temp_md_file = "article_temp.md"
with open(temp_md_file, "w", encoding="utf-8") as f:
    f.write(markdown_teksti)

# Määritellään PDF-tiedoston nimi
pdf_tiedosto = "artikkeli_direct_pandoc.pdf"

# Muunnetaan Markdown suoraan PDF:ksi käyttämällä Pandocia (Markdown -> LaTeX -> PDF)
# Huom! Varmista, että pdflatex (tai xelatex, mikäli haluat) on asennettuna.
extra_args = ["--pdf-engine=pdflatex"]  # Vaihtoehtoisesti käytä xelatexia: ["--pdf-engine=xelatex"]
pypandoc.convert_file(temp_md_file, "pdf", outputfile=pdf_tiedosto, extra_args=extra_args)

print(f"PDF-tiedosto luotu: {pdf_tiedosto}")