import requests
from bs4 import BeautifulSoup

from expand import expand_table

def scrape_aw():
    url = "https://fieldsofmistria.wiki.gg/wiki/Archaeology_Wing"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # sets
    # format {
    #           set name: [
    #              { name: ,
    #                img_url: ,
    #                loc: ,
    #                rarity: ,
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

                rows = [] # list of rows in each set
                for row in grid[1:]: # cols in each row : name, img_url, location, rarity, completed

                    link_tag = row[0].find("a")
                    img_tag = link_tag.find("img")
                    img_url = "https://fieldsofmistria.wiki.gg" + img_tag.get("src") # to account for lazy loading

                    name = row[1].get_text(strip=True)
                    location = row[2].get_text(separator=" ", strip=True)
                    rarity = row[3].get_text(strip=True)

                    rows.append({
                        "name": name,
                        "img_url": img_url,
                        "location": location,
                        "rarity": rarity,
                        "completed": False # default
                    })

                sets[set_name] = rows

    return sets