import json
import re
from pathlib import Path

IMAGE_FOLDER = Path("images")
OUTPUT_FILE = Path("gallery.json")

data = []

if not IMAGE_FOLDER.exists():
    print("❌ Le dossier images n'existe pas")
    raise SystemExit

pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:d(\d+))?$", re.IGNORECASE)

for file in sorted(IMAGE_FOLDER.iterdir()):
    if file.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
        continue

    match = pattern.match(file.stem)

    # Ignore fond.png et profil.png automatiquement
    if not match:
        print("Ignorée :", file.name)
        continue

    date = match.group(1)
    dessin_num = match.group(2)

    order = int(dessin_num) if dessin_num else 1

    title = date if order == 1 else f"{date} — dessin {order}"
    description = (
        f"Illustration du {date}."
        if order == 1
        else f"Illustration du {date}, dessin {order}."
    )

    data.append({
        "title": title,
        "description": description,
        "image": file.as_posix(),
        "date": date,
        "order": order
    })

data.sort(key=lambda item: (item["date"], item["order"]))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ gallery.json créé avec {len(data)} image(s)")