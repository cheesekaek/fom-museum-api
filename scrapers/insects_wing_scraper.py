import requests
from bs4 import BeautifulSoup

from utils import expand_table, get_header_indices


def scrape_iw():
    url = "https://fieldsofmistria.wiki.gg/wiki/Insects_Wing"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # sets
    # format {
    #           set name: [
    #              { name: ,
    #                img_url: ,
    #                location: ,
    #                season: ,
    #                time: ,
    #                weather: ,
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

                indices = get_header_indices(set_table) # col indices
                image_index = indices.get("image")
                name_index = indices.get("name")
                location_index = indices.get("location")
                season_index = indices.get("season") # check if season present
                time_index = indices.get("time")
                weather_index = indices.get("weather")
                rarity_index = indices.get("rarity") # check if rarity present

                for row in grid[1:]:

                    link_tag = row[image_index].find("a")
                    img_tag = link_tag.find("img")
                    img_url = "https://fieldsofmistria.wiki.gg" + img_tag.get("src") # to account for lazy loading

                    name = row[name_index].get_text(strip=True)
                    location = row[location_index].get_text(separator=" ", strip=True)

                    seasons = set()
                    if season_index is not None:
                        a_tags = row[season_index].find_all("a")
                        if a_tags:
                            for a in a_tags:
                                text = a.get_text(strip=True)
                                if text:
                                    seasons.add(text)
                        else:
                            text = row[season_index].get_text(strip=True)
                            if text:
                                seasons.add(text)
                    else:
                        if set_name in ("Spring", "Summer", "Winter", "Fall"):
                            seasons.add(set_name)
                        else:
                            seasons.add("All")

                    span_tags = row[time_index].find_all("span", class_="no-wrap")
                    time_range = span_tags[-1].get_text(strip=True).replace("\xa0", " ") # just the time range

                    a_tags = row[weather_index].find_all("a", title="Weather")
                    weather = set()
                    if a_tags:
                        for a in a_tags:
                            text = a.get_text(strip=True)
                            if text:
                                weather.add(text)

                    if rarity_index is not None:
                        rarity = row[rarity_index].get_text(strip=True)
                    else:
                        rarity = set_name

                    rows.append({
                        "name": name,
                        "img_url": img_url,
                        "location": location,
                        "season(s)": seasons,
                        "time_range": time_range,
                        "weather": weather,
                        "rarity": rarity,
                        "completed": False # default
                    })

                sets[set_name] = rows

    return sets