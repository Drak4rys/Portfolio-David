from __future__ import annotations

import json
import re
from pathlib import Path

IMAGES_DIR = Path("images")
OUTPUT_FILE = Path("gallery.json")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Formats acceptés :
# 2025-05-07.jpg
# 2025-05-07d1.png
# 2025-05-07d2.webp
FILENAME_PATTERN = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})(?:d(?P<order>\d+))?$")


def parse_filename(file_path: Path) -> tuple[str, int]:
    stem = file_path.stem.strip()
    match = FILENAME_PATTERN.match(stem)

    if not match:
        return ("1900-01-01", 0)

    date_value = match.group("date")
    order_value = match.group("order")
    order = int(order_value) if order_value is not None else 0
    return (date_value, order)


def build_title(date_value: str, order: int) -> str:
    if order == 0:
        return date_value
    return f"{date_value} — dessin {order}"


def build_description(date_value: str, order: int) -> str:
    if order == 0:
        return f"Illustration du {date_value}."
    return f"Illustration du {date_value}, dessin {order}."


def scan_images(images_dir: Path) -> list[dict]:
    if not images_dir.exists():
        raise FileNotFoundError(f"Le dossier '{images_dir}' est introuvable.")

    files = [
        file_path
        for file_path in images_dir.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in ALLOWED_EXTENSIONS
    ]

    parsed_files = []
    for file_path in files:
        date_value, order = parse_filename(file_path)
        parsed_files.append((date_value, order, file_path))

    # Tri du plus ancien au plus récent, puis par numéro de dessin dans la journée
    parsed_files.sort(key=lambda item: (item[0], item[1], item[2].name.lower()))

    artworks = []
    for date_value, order, file_path in parsed_files:
        artworks.append(
            {
                "title": build_title(date_value, order),
                "description": build_description(date_value, order),
                "image": file_path.as_posix(),
                "date": date_value,
                "order": order,
            }
        )

    return artworks


def save_gallery_json(artworks: list[dict], output_file: Path) -> None:
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(artworks, f, ensure_ascii=False, indent=2)


def main() -> None:
    artworks = scan_images(IMAGES_DIR)
    save_gallery_json(artworks, OUTPUT_FILE)
    print(f"gallery.json généré avec {len(artworks)} image(s).")


if __name__ == "__main__":
    main()