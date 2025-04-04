#!/usr/bin/env python3
import argparse
import sys
import os
import re
import requests
import csv
import PyPDF2  
import pandas as pd
from docx import Document
from html.parser import HTMLParser
from openai import OpenAI

client = OpenAI()

MODEL = "gpt-4o"
TEMPERATURE = 0.7
MAX_TOKENS = 1000

# HTML
class TextExtractHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.ignore_tags = {'script', 'style', 'meta', 'head', 'title', 'link'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        if self.current_tag == tag:
            self.current_tag = None

    def handle_data(self, data):
        if self.current_tag not in self.ignore_tags:
            text = data.strip()
            if text:
                self.text.append(text)

    def get_text(self):
        return '\n'.join(self.text)

# Luku- ja esikäsittely
def extract_text_from_pdf(path):
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        print(f"[ERROR] PDF: {e}", file=sys.stderr)
        sys.exit(1)

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_csv(path):
    df = pd.read_csv(path)
    return df.to_string(index=False)

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '').lower()
        if 'text/html' not in content_type:
            print(f"URL ei ole HTML-sivu (Content-Type: {content_type})", file=sys.stderr)
            sys.exit(1)
        parser = TextExtractHTMLParser()
        parser.feed(response.text)
        return parser.get_text()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] URL: {e}", file=sys.stderr)
        sys.exit(1)

def query_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Olet tehokas assistentti, joka tekee tiivistelmiä antamistani dokumenteista."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    return response.choices[0].message.content.strip()

def extract_text(path):
    if re.match(r'^https?://', path, re.IGNORECASE):
        return extract_text_from_url(path)
    if not os.path.exists(path):
        print(f"[ERROR] File '{path}' not found.", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext == ".txt":
        return extract_text_from_txt(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    elif ext == ".csv":
        return extract_text_from_csv(path)
    else:
        print(f"[ERROR] Unsupported file type: {ext}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Feed one or more inputs to LLM (txt, pdf, docx, csv, URL).")
    parser.add_argument("inputs", nargs="+", help="Files or URLs")
    parser.add_argument("-q", "--query", help="Custom prompt (default: summarize the content in Markdown format)")
    parser.add_argument("-o", "--output", help="Write response to file")

    args = parser.parse_args()

    markdown_text = ""
    for input_path in args.inputs:
        text = extract_text(input_path)
        markdown_text += f"## 📄 Lähde: `{input_path}`\n\n{text}\n\n"

    if not markdown_text.strip():
        print("[ERROR] Ei tietoa", file=sys.stderr)
        sys.exit(1)

    prompt = args.query or f"Tiivistä seuraava sisältö Markdown-muodossa:\n\n{markdown_text}"
    print("[INFO] Tiedostoa käsitellään...")
    result = query_llm(prompt)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"[INFO] Markdown-output tallennettu tiedostoon: {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()