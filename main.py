import json
from pathlib import Path

from starlette.responses import JSONResponse

from scrapers.fish_wing_scraper import scrape_fw
from scrapers.archaeology_wing_scraper import scrape_aw
from scrapers.flora_wing_scraper import scrape_flw
from scrapers.insects_wing_scraper import scrape_iw

from fastapi import FastAPI, HTTPException

app = FastAPI()

MUSEUM_WINGS = {
    "fish-wing": scrape_fw,
    "archaeology-wing": scrape_aw,
    "flora-wing": scrape_flw,
    "insects-wing": scrape_iw
}

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_json_file(filename: str, data: dict):
    path = DATA_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=list)
    return path

# individual wing scraper
@app.post("/generate/{wing}")
def generate_wing(wing: str):
    if wing not in MUSEUM_WINGS:
        raise HTTPException(status_code=404, detail=f"'{wing}' is not a valid wing. Format: [wing-type]-wing")
    data = MUSEUM_WINGS[wing]()
    save_json_file(f"{wing}.json", data)
    return JSONResponse({"message": f"{wing}.json generated", "sets": list(data.keys())})

# JSON file refresher
@app.post("/refresh/{wing}")
def refresh_wing(wing: str):
    if wing not in MUSEUM_WINGS:
        raise HTTPException(status_code=404, detail=f"'{wing}' is not a valid wing. Format: [wing-type]-wing")
    data = MUSEUM_WINGS[wing]()
    save_json_file(f"{wing}.json", data)
    return JSONResponse({"message": f"{wing}.json refreshed", "sets": list(data.keys())})

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