from pydantic import BaseModel, ConfigDict


# app.get("/wings")
class ItemModel(BaseModel):
    # from_attributes=True for model_validate to work
    model_config = ConfigDict(from_attributes=True)
    # common attr
    id: int
    name: str
    img: str | None
    completed: bool
    # varied attr
    locations: list[str] | None
    rarity: str | None
    weather: list[str] | None
    size: str | None
    sources: list[str] | None
    seasons: list[str] | None
    time: str | None

class ItemSetModel(BaseModel):
    # from_attributes=True for model_validate to work
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    items: list[ItemModel] = []

class WingModel(BaseModel):
    id: int
    name: str
    sets: list[ItemSetModel] = []
    items: list[ItemModel] = []

# BaseModel used in app.get("/wings")
class IncludeSetItems(BaseModel):
    sets: bool = False
    items: bool = False

# BaseModel used in app.patch("/items/{item_id}")
class ItemUpdate(BaseModel):
    completed: bool