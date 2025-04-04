
import argparse
from openai import OpenAI
from file_util import fetch_url, save_binary_file, find_new_file_name

client = OpenAI()

# Kuvakoon muunnostaulukko
ASPECT_RATIO_TO_SIZE = {
    "1:1": "1024x1024",
    "16:9": "1792x1024",
    "4:3": "1408x1056",
    "3:4": "1056x1408"
}

def generate_images(prompt, aspect_ratio, n, style, quality):
    size = ASPECT_RATIO_TO_SIZE.get(aspect_ratio, "1024x1024")
    
    print(f"[INFO] Luodaan {n} kuva(a) koossa {size}...")

    urls = []
    for _ in range(n):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1 
        )
        image_url = response.data[0].url
        urls.append(image_url)
        print(f"[INFO] Kuva luotu: {image_url}")

        # Ladataan ja tallennetaan kuva
        image_data = fetch_url(image_url)
        if image_data is not None:
            file_name = find_new_file_name("dalle.png")
            if save_binary_file(image_data, file_name):
                print(f"[INFO] Kuva tallennettu: {file_name}")
        else:
            print("[WARN] Kuvan lataus epäonnistui.")

    return urls

def main():
    parser = argparse.ArgumentParser(description="Kuvageneraattori (DALL·E 3) komentoriviltä.")
    parser.add_argument("-p", "--prompt", required=True, help="Kuvaprompti (esim. 'photo of a cat on the moon')")
    parser.add_argument("-n", "--num_images", type=int, default=1, help="Luotavien kuvien määrä (max 4 suositeltu)")
    parser.add_argument("-a", "--aspect", choices=ASPECT_RATIO_TO_SIZE.keys(), default="1:1", help="Kuvan kuvasuhde")
    parser.add_argument("-s", "--style", choices=["natural", "vivid"], default="natural", help="Tyyli")
    parser.add_argument("-q", "--quality", choices=["standard", "hd"], default="hd", help="Laatu")

    args = parser.parse_args()

    generate_images(
        prompt=args.prompt,
        aspect_ratio=args.aspect,
        n=args.num_images,
        style=args.style,
        quality=args.quality
    )

if __name__ == "__main__":
    main()
