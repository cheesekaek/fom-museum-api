# fom-museum-api (❁´◡`❁)

A Python scraper and API for [Fields of Mistria](https://fieldsofmistria.wiki.gg/) that scrapes data from the wiki for all items that can be donated to the in-game museum. This data is provided via a FastAPI backend, with JSON datasets available for reference and/or further use.

---

## Project Structure ＼(ﾟｰﾟ＼)
```
fom-museum-api/
│
├── app/ # Models and script to populate database + base models to work with API routes
├── data/ # Generated JSON datasets using scrapers
├── scrapers/ # Scrapers for each wing + image scraper for each img url stored in JSON
├── static/images # all static images generated and stored here
├── .gitignore
├── main.py # API entrypoint
├── README.md
├── database.db # database generated 
└── requirements.txt # packages txt
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
|------------------------|------------------------------------------------------|
| `GET /wings`           | List all wings + sets and/or items                   |
| `GET /items/{item_id}` | Mark a specific item as completed/incomplete         |
| `GET /sets/{set_id}`   | Mark a specific set as completed/incomplete          |
| `GET /`                | List all available endpoints for scrapers            |
| `GET /generate/{wing}` | Scrapes data and generates JSON for a specific wing  |
| `GET /refresh/{wing}`  | Re-scrapes data and updates JSON for a specific wing |


Valid {wing} names:
insects-wing, fish-wing, archaeology-wing, flora-wing

---

## WIP (●'◡'●)
* change image name in db with 's to just s
* change json static to /static
* load database with new img url /static
* after change, change the frontend item row to just src={item.img}
* Update ```GET \``` to include endpoints for the API routes
* Frontend 💔
* frontend ideas : each wing has a link back to home page
* Possibly more API routes depending on how my frontend turns out

---

## Why I made this project ( ´･･)ﾉ(._.`) 
I spent hundreds of hours in this game, and have 100% multiple save files. On a recent update of this game, I realized that the trackers I used to note the items I collected before were super outdated, so I thought, "Hey, ik a thing or two about coding. Maybe I should make my own." This project is still a huge WIP, but I hope to complete it before I finish my 4th playthrough of this game haha. 


ps: yes i used ChatGPT to structure this README don't come after me! /_ \
