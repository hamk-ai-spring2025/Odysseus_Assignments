from openai import OpenAI

# Openaikey käyttöön
client = OpenAI()

# Parametrit
MODEL = "gpt-4"
TEMPERATURE = 0.9
MAX_TOKENS = 1000

SYSTEM_PROMPT = (
    "Olet huippuluova sisällöntuottaja, joka kirjoittaa koukuttavaa ja hakukoneystävällistä sisältöä. "
    "Hyödynnä runsaasti synonyymejä ja värikkäitä sanavalintoja, jotta sisältö erottuu ja menestyy hakukonetuloksissa."
)

def generate_variants(user_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        n=3
    )

    return [choice.message.content for choice in response.choices]

def main():
    print("Olen copywriter-kaverisi - luon antamastasi aiheesta hienoa sisältöä")
    user_prompt = input("Anna aihe: ")

    print("\nLuodaan luovia hakukoneoptimoituja versioita...\n")
    outputs = generate_variants(user_prompt)

    for i, text in enumerate(outputs, 1):
        print(f"\n--- Versio {i} ---\n{text}\n")

if __name__ == "__main__":
    main()

