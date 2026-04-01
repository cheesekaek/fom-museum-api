# fom-museum-api (❁´◡`❁)

A Python scraper and API for [Fields of Mistria](https://fieldsofmistria.wiki.gg/) that scrapes data from the wiki for all items that can be donated to the in-game museum. This data is provided via a FastAPI backend, with JSON datasets available for reference and/or further use.

---

## Project Structure ＼(ﾟｰﾟ＼)
```
fom-museum-api/
│
├── data/ # Generated JSON datasets used by the API
├── scrapers/ # Scripts for each scraper, corresponding to each museum wing (insects, fish, flora, archaeology)
├── .gitignore # gitignore ( ͠° ͟ʖ ͡°)
├── main.py # API entrypoint
└── README.md # The one you're reading rn ;)
```
---

## To run the API O(∩_∩)O

```bash
uvicorn main:app --reload
```

---

## Documentation .______.

Swagger UI:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Endpoints ⊙.☉
| Endpoint               | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| `GET /`                | List all available endpoints and wings               |
| `GET /generate/{wing}` | Scrapes data and generates JSON for a specific wing  |
| `GET /generate/all`    | Scrapes data and generates JSON for all wings        |
| `GET /refresh/{wing}`  | Re-scrapes data and updates JSON for a specific wing |
| `GET /refresh/all`     | Re-scrapes data and updates JSON for all wings       |

Valid {wing} names:
insects-wing, fish-wing, archaeology-wing, flora-wing

---

## WIP (●'◡'●)
* Wings: ```insects_wing_scraper``` hasn’t been fully tested
* Endpoints: ```/refresh/all``` hasn't been tested


---

## Why I made this project ( ´･･)ﾉ(._.`) 
I spent hundreds of hours in this game, and have 100% multiple save files. On a recent update of this game, I realized that the trackers I used to note the items I collected before were super outdated, so I thought, "Hey, ik a thing or two about coding. Maybe I should make my own." This project is still a huge WIP, but I hope to complete it before I finish my 4th playthrough of this game haha. 


ps: yes i used ChatGPT to structure this README don't come after me! /_ \
