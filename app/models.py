from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field, create_engine, Relationship


# wings
class Wing(SQLModel, table=True):
    id: int | None = Field(default=None,
                           primary_key=True)
    name: str = Field(index=True)
    # Relationship : sets
    sets: list["ItemSet"] = Relationship(back_populates="wing")


# each set in a wing
class ItemSet(SQLModel, table=True):
    __tablename__ = "item_set"
    id: int | None = Field(default=None,
                           primary_key=True)
    name: str = Field(index=True)
    # Relationship : wings
    wing_id: int | None = Field(default=None,
                                index=True,
                                foreign_key="wing.id")  # id column in wing
    wing: Wing = Relationship(back_populates="sets")
    # Relationship : items
    items: list["Item"] = Relationship(back_populates="item_set")


# each item in a set
class Item(SQLModel, table=True):
    id: int | None = Field(default=None,
                           primary_key=True)
    # common attributes across all items
    name: str = Field(index=True)
    img: str | None = None
    completed: bool = False
    # varying attributes across all items
    locations: list[str] | None = Field(default=None,
                                        sa_column=Column(JSON))
    rarity: str | None = None
    weather: list[str] | None = Field(default=None,
                                      sa_column=Column(JSON))
    size: str | None = None
    sources: list[str] | None = Field(default=None,
                                      sa_column=Column(JSON))
    seasons: list[str] | None = Field(default=None,
                                      sa_column=Column(JSON))
    time: str | None = None

    # Relationship : sets
    set_id: int | None = Field(default=None,
                               index=True,
                               foreign_key="item_set.id")  # id column in item_set
    item_set: ItemSet = Relationship(back_populates="items")



