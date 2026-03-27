import requests
from bs4 import BeautifulSoup

from scrapers.utils import expand_table


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

                rows = [] # list of rows in each set
                for row in grid[1:]: # cols in each row : name, img_url, location, rarity, completed

                    link_tag = row[0].find("a")
                    img_tag = link_tag.find("img")
                    img_url = "https://fieldsofmistria.wiki.gg" + img_tag.get("src") # to account for lazy loading

                    name = row[1].get_text(strip=True)

                    p_tag = row[2].find("p")
                    sources = set() # multiple sources
                    for a_tag in p_tag.find_all("a"):
                        source = a_tag.get("title")
                        if source and not source.startswith("Mines/") and source not in ("Combat", "Mining", "Magic Spells"):
                            # ^ removed redundant/unnecessary terms
                            sources.add(source)

                    locations = set() # multiple locations
                    curr_loc = [] # to account for different tag types for each location
                    for child in row[3].children:
                        if child.name == "a": # new location begins at a
                            if curr_loc:
                                locations.add(" ".join(curr_loc).strip()) # join curr loc and add to set
                                curr_loc = [] # refresh
                            curr_loc.append(child.get_text(strip=True))
                        elif child.name == "br": # skip br
                            continue
                        elif child.name == "small":
                            text = child.get_text(separator=" ", strip=True)
                            if text:
                                curr_loc.append(text)
                        else:  # plain text nodes
                            text = str(child).strip() # plain text
                            if text:
                                curr_loc.append(text)

                    if curr_loc:  # last group accounted for
                        locations.add(" ".join(curr_loc).strip())

                    rows.append({
                        "name": name,
                        "img_url": img_url,
                        "source(s)": sources,
                        "known_location(s)": locations,
                        "completed": False # default
                    })

                sets[set_name] = rows

    return sets