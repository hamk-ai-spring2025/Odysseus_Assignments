import os
import markdown2
import pdfkit
import anthropic

# Aihe
aihe = "Tekoälyn käyttö yläkoulussa: mahdollisuudet ja haasteet"

# API
api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)

# Claude
viesti = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=2000,
    system="Vastaa vain Markdown-muodossa. Kirjoita tieteellinen artikkeli suomeksi, jossa on Tiivistelmä, Johdanto, Luvut, Alaluvut, Johtopäätös ja APA-viitteet. Lisää yksi taulukko, jos mahdollista.",
    messages=[
        {
            "role": "user",
            "content": f"Kirjoita tieteellinen artikkeli aiheesta '{aihe}'. Käytä APA-viitteitä ja Markdown-muotoilua."
        }
    ]
)

markdown_teksti = viesti.content[0].text

# Markdown ->  HTML
html_sisalto = markdown2.markdown(markdown_teksti)

# HTML-muotoon CSS
html_valmis = f"""
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 40px;
        line-height: 1.6;
    }}
    h1, h2, h3 {{
        color: #2e3b4e;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }}
    table, th, td {{
        border: 1px solid #444;
        padding: 8px;
        text-align: left;
    }}
</style>
<title>{aihe}</title>
</head>
<body>
{html_sisalto}
</body>
</html>
"""

# Väliaikainen HTML
html_tiedosto = "artikkeli.html"
with open(html_tiedosto, "w", encoding="utf-8") as f:
    f.write(html_valmis)

# PDF-tiedosto
pdf_tiedosto = "artikkeli.pdf"

# wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Konfiguroi pdfkit
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# PDF
pdfkit.from_file(html_tiedosto, pdf_tiedosto, configuration=config)

print(f"\n PDF-tiedosto luotu: {pdf_tiedosto}")
