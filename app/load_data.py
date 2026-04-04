import json

from app.database import create_db_and_tables, engine
from app.models import *
from sqlmodel import Session

def main():
    create_db_and_tables()

    with Session(engine) as session:
        all_wings = [
            ("data/archaeology-wing.json", "Archaeology"),
            ("data/fish-wing.json", "Fish"),
            ("data/flora-wing.json", "Flora"),
            ("data/insects-wing.json", "Insects")
        ]

        for json_path, wing_name in all_wings:
            with open(json_path) as f:
                data = json.load(f)

            # set Wing
            wing = Wing(name=wing_name)
            # set ItemSet
            for set_name in data.keys():
                items = data.get(set_name)
                item_set = ItemSet(name=set_name,
                                   wing=wing)
                # set Item
                for item in items:
                    new_item = Item(
                        # all item attributes
                        name = item.get("name"),
                        img = item.get("img_url"),
                        # completed is already default False
                        locations = item.get("location(s)"),
                        rarity = item.get("rarity"),
                        weather = item.get("weather"),
                        size = item.get("size"),
                        sources = item.get("source(s)"),
                        seasons = item.get("season(s)"),
                        time = item.get("time_range"),
                        item_set=item_set
                    )
                    session.add(new_item)
        session.commit()

if __name__ == "__main__":
    main()






