import json
import time
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image


# Image scraper to download images (since these images not included in repo)
# use after downloading the JSON files for all 4 wings

all_wings = [
    ("data/archaeology-wing.json", "Archaeology"),
    ("data/fish-wing.json", "Fish"),
    ("data/flora-wing.json", "Flora"),
    ("data/insects-wing.json", "Insects")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

for json_path, wing_name in all_wings:
    with open(json_path) as f:
        data = json.load(f)

    IMAGES_DIR = Path(f"static/images/{wing_name.lower()}")
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for set_name, items in data.items(): # for every set
        for item in items: # access each item
            url = item.get("img_url")
            if not url:
                continue

            img_filename = url.split("/")[-1].split("?")[0] # formatted like img_name.png
            dest = IMAGES_DIR / img_filename
            # if img already downloaded
            if dest.exists():
                continue

            success = False
            for attempt in range(3):
                try:
                    response = requests.get(url, headers=headers, timeout=10)

                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content)) # content in dir(response)
                        img.save(str(dest)) # dest exists as Path so convert to str
                        success = True
                        break
                    else:
                        print(f"[FAIL] ({response.status_code}) [Attempt {attempt+1}]: {url}")
                except Exception as e:
                    print(f"[ERROR] ({e}) [Attempt {attempt+1}]: {url}")

                time.sleep(5)

            if success:
                item["img_url"] = dest.as_posix() # filepath added to JSON
            else:
                print(f" Failed to download: {url}") # mention failed download in JSON

    # update json
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)