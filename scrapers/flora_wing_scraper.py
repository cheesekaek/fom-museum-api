import requests
from bs4 import BeautifulSoup

from scrapers.utils import expand_table, parse_locations, get_header_indices


def scrape_flw():
    url = "https://fieldsofmistria.wiki.gg/wiki/Flora_Wing"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # sets
    # format {
    #           set name: [
    #              { name: ,
    #                img_url: ,
    #                sources: ,
    #                locations: ,
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
                sources_index = indices.get("source(s)")
                location_index = indices.get("known location(s)")

                rows = [] # list of rows in each set
                for row in grid[1:]: # cols in each row : name, img_url, location, rarity, completed

                    link_tag = row[image_index].find("a")
                    img_tag = link_tag.find("img")
                    img_url = "https://fieldsofmistria.wiki.gg" + img_tag.get("src") # to account for lazy loading

                    name = row[name_index].get_text(strip=True)

                    p_tag = row[sources_index].find("p")
                    sources = set() # multiple sources
                    for a_tag in p_tag.find_all("a"):
                        source = a_tag.get("title")
                        if source and not source.startswith("Mines/") and source not in ("Combat", "Mining", "Magic Spells"):
                            # ^ removed redundant/unnecessary terms
                            sources.add(source)

                    locations = parse_locations(row[location_index])
                    final_loc = [] # custom modification for inconsistent HTML formats
                    text = ""
                    for loc in locations:
                        if loc.startswith("(floors") | loc.startswith("* Underseaweed"):
                            pass  # skips these locations
                        elif loc == "(Requires Void Sight)":
                            text += f" {loc}"
                        else:
                            final_loc.append(loc)
                    final_loc = [loc + text if loc == "Any Floor Without a Seal" else loc for loc in final_loc]

                    rows.append({
                        "name": name,
                        "img_url": img_url,
                        "source(s)": sources,
                        "known_location(s)": final_loc,
                        "completed": False # default
                    })

                sets[set_name] = rows

    return sets