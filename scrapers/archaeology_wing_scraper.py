import requests
from bs4 import BeautifulSoup

from scrapers.utils import expand_table, parse_locations, get_header_indices

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

                indices = get_header_indices(set_table) # indices for cols
                name_index = indices.get("name")
                image_index = indices.get("image")
                location_index = indices.get("location")
                rarity_index = indices.get("rarity")

                rows = [] # list of rows in each set
                for row in grid[1:]: # cols in each row : name, img_url, location, rarity, completed

                    link_tag = row[image_index].find("a")
                    img_tag = link_tag.find("img")
                    img_url = "https://fieldsofmistria.wiki.gg" + img_tag.get("src") # to account for lazy loading

                    name = row[name_index].get_text(strip=True)

                    locations = parse_locations(row[location_index])
                    final_loc = [] # custom modification for inconsistent HTML formats
                    text = ""
                    for loc in locations:
                        if loc.startswith("(floors"):
                            pass  # skip floor ranges entirely
                        elif loc == "(requires Former Farmers Skill)":
                            text += f" {loc}"
                        else:
                            final_loc.append(loc)
                    final_loc = [loc + text if loc == "The Farm" else loc for loc in final_loc]

                    rarity = row[rarity_index].get_text(strip=True)

                    rows.append({
                        "name": name,
                        "img_url": img_url,
                        "location(s)": final_loc,
                        "rarity": rarity,
                        "completed": False # default
                    })

                sets[set_name] = rows

    return sets