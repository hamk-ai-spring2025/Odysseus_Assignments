import openai
import argparse

from openai import OpenAI

# Luo asiakasolio (API-avain luetaan oletuksena ympäristömuuttujasta OPENAI_API_KEY)
client = OpenAI()

def generate_creative_content(prompt, num_versions=3):
    """
    Generate creative content using OpenAI's GPT model.
    Produces multiple versions of the content with SEO optimization.
    """
    try:
        responses = []
        for _ in range(num_versions):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a creative writer specializing in marketing materials, memes, song lyrics, poems, and SEO-optimized blog posts. Use as many synonyms as possible to enhance search engine optimization."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,  # Adjust for creativity
                top_p=0.9,         # Nucleus sampling
                presence_penalty=0.6,  # Encourage new ideas
                frequency_penalty=0.4  # Reduce repetition
            )
            responses.append(response.choices[0].message.content)
        return responses
    except openai.error.OpenAIError as e:
        return [f"Error: {str(e)}"]

def main():
    parser = argparse.ArgumentParser(description="Creative Writer CLI using OpenAI LLM")
    parser.add_argument("prompt", type=str, help="The prompt for the creative writer")
    parser.add_argument("--versions", type=int, default=3, help="Number of versions to generate (default: 3)")
    args = parser.parse_args()

    print("Generating creative content...\n")
    results = generate_creative_content(args.prompt, args.versions)
    for i, result in enumerate(results, 1):
        print(f"Version {i}:\n{result}\n{'-'*40}\n")

if __name__ == "__main__":
    main()