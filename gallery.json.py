import os
import json
from pathlib import Path

IMAGE_FOLDER = Path("images")

data = []

if not IMAGE_FOLDER.exists():
    print("❌ Le dossier images n'existe pas")
    exit()

# Tri des fichiers pour un ordre stable
files = sorted(IMAGE_FOLDER.iterdir())

for file in files:
    if file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        print("Image trouvée :", file.name)

        data.append({
            "image": str(file),
            "title": file.stem,  # nom sans extension
            "description": "",
            "date": ""
        })

# Écriture JSON
with open("gallery.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ gallery.json créé avec {len(data)} image(s)")