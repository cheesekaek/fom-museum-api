import json
from pathlib import Path
from typing import Annotated

from sqlmodel import Session, select
from starlette.responses import JSONResponse

from app.database import get_session
from app.models import Wing
from scrapers.fish_wing_scraper import scrape_fw
from scrapers.archaeology_wing_scraper import scrape_aw
from scrapers.flora_wing_scraper import scrape_flw
from scrapers.insects_wing_scraper import scrape_iw

from fastapi import FastAPI, HTTPException, Depends, Query

app = FastAPI()


# ---------------------------------------------------
# -------------------- API ROUTES -------------------
# ---------------------------------------------------


@app.get("/wings")
def get_wings(session: Session = Depends(get_session),
              offset: int = 0,
              limit: Annotated[int, Query(le=4)] = 4):

    wings = session.exec(select(Wing).offset(offset).limit(limit)).all()

    result = []

    for wing in wings:
        # wing attributes
        wing_data = {
            "id": wing.id,
            "name": wing.name,
            "sets": []
        }
        # set attributes
        for s in wing.sets:
            set_data = {
                "id": s.id,
                "name": s.name,
                "items": []
            }
            # item attributes
            for item in s.items:
                item_data = {
                    # common attr
                    "id": item.id,
                    "name": item.name,
                    "img": item.img,
                    "completed": item.completed,
                    # varied attr
                    "locations": item.locations,
                    "rarity": item.rarity,
                    "weather": item.weather,
                    "size": item.size,
                    "sources": item.sources,
                    "seasons": item.seasons,
                    "time": item.time
                }
                # add each item to set
                set_data["items"].append(item_data)
            # add each set to a wing
            wing_data["sets"].append(set_data)
        # add each wing to result
        result.append(wing_data)
    # return list
    return result




# ----------------------------------------------------
# --------------------- SCRAPERS ---------------------
# ----------------------------------------------------

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
        json.dump(data, f, indent=4)
    return path

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
