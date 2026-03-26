import os, json

from starlette.responses import JSONResponse

from fish_wing_scraper import scrape_fw
from archaeology_wing_scraper import scrape_aw
from flora_wing_scraper import scrape_flw
from insects_wing_scraper import scrape_iw

from fastapi import FastAPI, HTTPException

app = FastAPI()

MUSEUM_WINGS = {
    "fish-wing": scrape_fw,
    "archaeology-wing": scrape_aw,
    "flora-wing": scrape_flw,
    "insects-wing": scrape_iw
}

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_json_file(f: str, data: dict):
    path = os.path.join(DATA_DIR, f)
    with open(path, "w") as filename:
        json.dump(data, filename, indent=4, default=list)
    return path

# individual wing scraper
@app.post("/generate/{wing}")
def generate_wing(wing: str):
    if wing not in MUSEUM_WINGS:
        raise HTTPException(status_code=404, detail=f"'{wing}' is not a valid wing. Format: [wing-type]-wing")
    data = MUSEUM_WINGS[wing]()
    save_json_file(f"{wing}.json", data)
    return JSONResponse({"message": f"{wing}.json generated", "sets": list(data.keys())})

# individual wing JSON file refresher
@app.post("/refresh/{wing}")
def refresh_wing(wing: str):
    if wing not in MUSEUM_WINGS:
        raise HTTPException(status_code=404, detail=f"'{wing}' is not a valid wing. Format: [wing-type]-wing")
    data = MUSEUM_WINGS[wing]()
    save_json_file(f"{wing}.json", data)
    return JSONResponse({"message": f"{wing}.json refreshed", "sets": list(data.keys())})

# combined wings scraper
@app.post("/generate/all")
def generate_all():
    combined = {}
    for wing, scraper in MUSEUM_WINGS.items():
        data = scraper()
        save_json_file(f"{wing}.json", data)
        combined[wing] = data
    save_json_file("all_wings.json", combined)
    return JSONResponse({"message": "all_wings.json generated", "wings": list(MUSEUM_WINGS.keys())})

# combined wings refresher
@app.post("/refresh/all")
def refresh_all():
    combined = {}
    for wing, scraper in MUSEUM_WINGS.items():
        data = scraper()
        save_json_file(f"{wing}.json", data)
        combined[wing] = data
    save_json_file("all_wings.json", combined)
    return JSONResponse({"message": "all_wings.json refreshed", "wings": list(MUSEUM_WINGS.keys())})

@app.get("/")
def hello():
    return {
        "generate_json_for": {
            "individual": "/generate/{wing}",
            "all": "/generate/all"
        },
        "refresh_json_for": {
            "individual": "/refresh/{wing}",
            "all": "/refresh/all"
        },
        "wings": list(MUSEUM_WINGS.keys())
    }