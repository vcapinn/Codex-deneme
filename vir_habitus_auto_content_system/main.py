"""Entry point for Vir Habitus Auto Content System."""

import os
import time
from pathlib import Path

from dotenv import load_dotenv

from drive_utils import get_service, list_images_in_folder, download_file
from gpt_utils import generate_post

# Folder ID on Google Drive containing images
FOLDER_ID = "1VFt73cldRpKQpgsohdlnBxCZa0nZEfYG"
# Check interval in seconds
CHECK_INTERVAL = 300
# Where to store generated posts and downloaded images
OUTPUT_DIR = Path("output")


def load_processed_list(path: Path) -> set:
    """Load the set of already processed file IDs."""
    if not path.exists():
        return set()
    return set(p.strip() for p in path.read_text().splitlines() if p.strip())


def save_processed_list(path: Path, processed: set) -> None:
    path.write_text("\n".join(sorted(processed)))


def process_new_images(service, processed: set, processed_path: Path) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    files = list_images_in_folder(service, FOLDER_ID)
    for file in files:
        file_id = file["id"]
        name = file["name"]
        if file_id in processed:
            continue
        print(f"Processing {name} ({file_id})")
        image_path = OUTPUT_DIR / name
        download_file(service, file_id, image_path)
        caption, title, hashtags = generate_post(image_path)
        idx = len(processed) + 1
        post_file = OUTPUT_DIR / f"post_{idx}.txt"
        with post_file.open("w", encoding="utf-8") as f:
            f.write(caption + "\n")
            f.write(title + "\n")
            f.write(hashtags + "\n")
        processed.add(file_id)
        save_processed_list(processed_path, processed)
        print(f"Saved post to {post_file}")


def main():
    load_dotenv()
    creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT")
    if not creds_path:
        raise SystemExit("GOOGLE_SERVICE_ACCOUNT env var not set")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise SystemExit("OPENAI_API_KEY env var not set")
    os.environ["OPENAI_API_KEY"] = openai_api_key
    service = get_service(Path(creds_path))
    processed_path = Path("processed_files.txt")
    processed = load_processed_list(processed_path)

    while True:
        process_new_images(service, processed, processed_path)
        print(f"Sleeping {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

