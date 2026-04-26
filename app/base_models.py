from typing import Optional

from pydantic import BaseModel, ConfigDict



# app.get("/wings")
class WingModel(BaseModel):
    id: int
    name: str


# app.get("/wings/{wing_id}")
class ItemModel(BaseModel):
    # common attr
    id: int
    name: str
    img: Optional[str]
    completed: bool
    # varied attr
    locations: Optional[list[str]]
    rarity: Optional[str]
    weather: Optional[list[str]]
    size: Optional[str]
    sources: Optional[list[str]]
    seasons: Optional[list[str]]
    time: Optional[str]

    # from_attributes=True for model_validate to work
    model_config = ConfigDict(from_attributes=True)


# app.get("/wings/{wing_id}")
class ItemSetModel(BaseModel):
    id: int
    name: str
    items: list[ItemModel] = None

    # from_attributes=True for model_validate to work
    model_config = ConfigDict(from_attributes=True)


# app.get("/wings/{wing_id}")
class WingModelExtra(BaseModel):
    id: int
    name: str
    sets: list[ItemSetModel] = None
    items: list[ItemModel] = None

    # from_attributes=True for model_validate to work
    model_config = ConfigDict(from_attributes=True)


# BaseModel used in app.patch("/items/{item_id}")
class ItemUpdate(BaseModel):
    completed: bool