"""Utilities for interacting with OpenAI GPT-4."""

from pathlib import Path
from typing import Tuple

import openai

# Template for the system prompt
SYSTEM_PROMPT = (
    "You are a social media content generator. "
    "Each image you receive is an inspirational post about a man's life system."\
    " Analyze the image and craft:\n"
    "1. A 200-word Instagram post caption in English.\n"
    "2. A short aphorism title.\n"
    "3. Exactly five high-engagement hashtags."
)


def generate_post(image_path: Path) -> Tuple[str, str, str]:
    """Generate caption, title and hashtags for the given image."""
    with image_path.open("rb") as img_file:
        image_bytes = img_file.read()

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "This visual is an inspirational post for a man's life system.",
                    },
                    {"type": "image", "image": image_bytes},
                ],
            },
        ],
    )

    content = response.choices[0].message.content
    # Split sections by newline for easier handling
    parts = [p.strip() for p in content.split("\n") if p.strip()]
    caption = parts[0]
    title = parts[1] if len(parts) > 1 else ""
    hashtags = parts[2] if len(parts) > 2 else ""
    return caption, title, hashtags

