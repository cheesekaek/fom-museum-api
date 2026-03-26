import requests
from bs4 import BeautifulSoup

from expand import expand_table


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
                headers = [th.get_text(strip=True).lower() for th in grid[0]] # list of all col names
                season_index = headers.index("season") if "season" in headers else None # check if season present
                time_index = headers.index("time")
                weather_index = headers.index("weather")
                rarity_index = headers.index("rarity")

                for row in grid[1:]:

                    link_tag = row[0].find("a")
                    img_tag = link_tag.find("img")
                    img_url = "https://fieldsofmistria.wiki.gg" + img_tag.get("src") # to account for lazy loading

                    name = row[1].get_text(strip=True)
                    location = row[2].get_text(separator=" ", strip=True)

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
                        seasons.add("All")

                    span_tags = row[time_index].find_all("span", class_="no-wrap")
                    time_range = span_tags[-1].get_text(strip=True) # just the time range

                    a_tags = row[weather_index].find_all("a", title="Weather")
                    weather = set()
                    if a_tags:
                        for a in a_tags:
                            text = a.get_text(strip=True)
                            if text:
                                weather.add(text)

                    rarity = row[rarity_index].get_text(strip=True)

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