import json
from pathlib import Path
from typing import Annotated

from sqlmodel import Session, select
from starlette.responses import JSONResponse

from app.base_models import WingModel, ItemUpdate, ItemModel, IncludeSetItems, ItemSetModel
from app.database import get_session
from app.models import Wing, Item, ItemSet
from scrapers.fish_wing_scraper import scrape_fw
from scrapers.archaeology_wing_scraper import scrape_aw
from scrapers.flora_wing_scraper import scrape_flw
from scrapers.insects_wing_scraper import scrape_iw

from fastapi import FastAPI, HTTPException, Depends, Query

app = FastAPI()


# ---------------------------------------------------
# -------------------- API ROUTES -------------------
# ---------------------------------------------------


# -------------------- GET /wings --------------------
@app.get("/wings", response_model=list[WingModel], description="Get a list of all wings, including sets or items, or both")
def get_wings(session: Session = Depends(get_session),
              # toggle to include sets or items, or both
              include: IncludeSetItems = Depends(),
              limit: Annotated[int, Query(ge=1, le=4)] = 4):

    wings = session.exec(select(Wing).limit(limit)).all()

    result = []

    for wing in wings:
        # wing attributes
        wing_data = {
            "id": wing.id,
            "name": wing.name,
        }

        # if sets is set to True
        if include.sets:
            wing_data["sets"] = []
            # set attributes
            for s in wing.sets:
                set_data = {
                    "id": s.id,
                    "name": s.name,
                }
                # if items is set to True
                if include.items:
                    # add each item to set
                    set_data["items"] = [ItemModel.model_validate(item) for item in s.items]
                # add each set to a wing
                wing_data["sets"].append(set_data)

        # if items is set to True
        elif include.items:
            wing_data["items"] = [
                ItemModel.model_validate(item)
                for s in wing.sets
                for item in s.items
            ]

        # add each wing to result
        result.append(wing_data)

    # return list
    return result


# ------------------ PATCH /items/{items_id} --------------------
@app.patch("/items/{item_id}", response_model=ItemModel, description="Mark an item as completed")
def update_item(update: ItemUpdate,
                item_id: int = 1,
                session: Session = Depends(get_session)):
    # find item
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="This item cannot be found.")

    # update item
    item.completed = update.completed
    session.commit()
    session.refresh(item)

    return ItemModel.model_validate(item)

# ------------------ PATCH /sets/{sets_id} --------------------
@app.patch("/sets/{sets_id}", response_model=ItemSetModel, description="Mark a set as completed")
def update_set(update: ItemUpdate,
               sets_id: int = 1,
               session: Session = Depends(get_session)):
    # find set
    item_set = session.get(ItemSet, sets_id)
    
    if not item_set:
        raise HTTPException(status_code=404, detail="This set cannot be found.")

    # find each item in set
    for item in item_set.items:
        # update item
        item.completed = update.completed

    session.commit()
    session.refresh(item_set)
    return ItemSetModel.model_validate(item_set)


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
