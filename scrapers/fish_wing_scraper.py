import re

import requests
from bs4 import BeautifulSoup

from utils import expand_table, get_header_indices

def scrape_fw():
    # fish wing url scraper
    url = "https://fieldsofmistria.wiki.gg/wiki/Fish_Wing"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')


    # sets
    # format {
    #           set name: [
    #              { name: ,
    #                img_url: ,
    #                loc: ,
    #                weather: ,
    #                rarity: ,
    #                size: ,
    #                completed: False
    #              }
    #           ], /.../
    #        }

    sets = {}
    for span in soup.find_all("span", class_="mw-headline"):
        if span.parent.name == "h3":
            set_name = span.get_text().strip() # set_name : key for set
            set_table = span.find_next("table") # set_table : val for set

            if set_table:
                grid = expand_table(set_table) # 2d grid

                indices = get_header_indices(set_table) # indices for cols
                name_index = indices.get("name")
                image_index = indices.get("image")
                location_index = indices.get("location")
                weather_index = indices.get("weather") # weather index check required
                rarity_index = indices.get("rarity")
                size_index = indices.get("size")

                rows = [] # list of rows in each set
                for row in grid[1:]: # cols in each row : name, img_url, location, weather, rarity, size, completed

                    link_tag = row[image_index].find("a")
                    img_tag = link_tag.find("img")
                    img_url = "https://fieldsofmistria.wiki.gg" + img_tag.get("src") # to account for lazy loading

                    name = row[name_index].get_text(strip=True)
                    location = row[location_index].get_text(separator=" ", strip=True)
                    location = re.sub(r"\s+\)", ")", location) # cleanup text "s+)" into ")"

                    if weather_index is not None:
                        a_tags = row[weather_index].find_all("a")
                        weather = set()
                        for a in a_tags:
                            text = a.get_text(strip=True)
                            if text:
                                weather.add(text)
                    else:
                        weather = "All"

                    if rarity_index is not None:
                        rarity = row[rarity_index].get_text(strip=True)
                    else:
                        rarity = set_name

                    size = row[size_index].get_text(strip=True)

                    rows.append({
                        "name": name,
                        "img_url": img_url,
                        "location": location,
                        "weather": weather,
                        "rarity": rarity,
                        "size": size,
                        "completed": False # default
                    })

                sets[set_name] = rows
    return sets