# fom-museum-api (❁´◡`❁)

A Python scraper and API for [Fields of Mistria](https://fieldsofmistria.wiki.gg/) that scrapes data from the wiki for all items that can be donated to the in-game museum. This data is provided via a FastAPI backend, with JSON datasets available for reference and/or further use.

---

## Project Structure ＼(ﾟｰﾟ＼)
```
fom-museum-api/
│
├── app/ # Models and script to populate database + base models to work with API routes
├── data/ # Generated JSON datasets using scrapers
├── frontend/ # Frontend
├── scrapers/ # Scrapers for each wing + image png scraper for each img url stored in JSON
├── static/images # all static images generated and stored here
├── .gitignore
├── database.db # database generated 
├── main.py # API entrypoint
├── README.md
└── requirements.txt # packages txt
```
---

## To run this project

```bash
python -m app.load_data
uvicorn main:app --reload
```
In another terminal, run
```bash
cd frontend
npm run dev
```
Go to this link: http://localhost:5173/

---

## To generate the JSON datasets + img files

```bash
uvicorn main:app --reload
```
Then, follow this link [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Generate each wing in ```POST```.
* Refresh each wing in ```POST``` if required.
* The datasets can be found in ```data/``` in the project root.
```bash
python scrapers/img_scraper.py
```
This creates a folder called ```static/``` that contains the image files. It renames the value of 'img_url' in the JSON
files (which are originally stored as URLs) to the location of these image files.

---

## Documentation

Swagger UI:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Endpoints ⊙.☉
| Endpoint               | Description                                          |
|------------------------|------------------------------------------------------|
| `GET /wings`           | List all wings                                       |
| `GET /wings/{wing_id}` | Get a specific wing, and its sets and items          |
| `GET /items/{item_id}` | Mark a specific item as complete/incomplete          |
| `GET /sets/{set_id}`   | Mark a specific set as completed/incomplete          |
| `GET /`                | List all available endpoints for scrapers            |
| `GET /generate/{wing}` | Scrapes data and generates JSON for a specific wing  |
| `GET /refresh/{wing}`  | Re-scrapes data and updates JSON for a specific wing |


Valid {wing} names for generating JSON:
insects-wing, fish-wing, archaeology-wing, flora-wing

---

## WIP (●'◡'●)
* Frontend for marking an entire set as complete

---

## Why I made this project ( ´･･)ﾉ(._.`) 
I spent hundreds of hours in this game, and have 100% multiple save files. 
On a recent update of this game, I realized that the trackers I used to note the items I collected 
before were super outdated, so I thought, "Hey, ik a thing or two about coding. Maybe I should make my own." 
And here it is!
