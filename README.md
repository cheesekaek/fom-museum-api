## fom-museum-api (❁´◡`❁)
A scraper for the https://fieldsofmistria.wiki.gg/ that collects data for all the items that can be donated to the in-game museum.

### DOCS 
For this project, I used FastAPI's built-in Swagger UI for testing the endpoints.

### RUN
bash: uvicorn main:app --reload

### DOCS
http://127.0.0.1:8000/docs

### ENDPOINTS (CURRENTLY AVAILABLE)
☆ `GET /` : List of endpoints + list of wings  
☆ `GET /generate/{wing}` : scrapes data and generates JSON for a specific wing  
☆ `GET /generate/all` : scrapes data and generates JSON for all wings  
☆ `GET /refresh/{wing}` : re-scrapes data and generates JSON for a specific wing  
☆ `GET /refresh/all` : -rescrapes data and generates JSON for all wings  

note: valid {wing} names are : 'insects-wing' , 'fish-wing' , 'archaeology-wing' , 'flora-wing'

### WIP (●'◡'●)
O In fishing-wing.json  
-> multiple weather elements not taken into account  
-> multiple location elements not taken into account  
-> in some sets, the weather column in absent. needs to be considered  

O Haven't tested archaeology, flora and fauna  

O Haven't tested refresher  

### why I made this project  
I spent hundreds of hours in this game, and have 100% multiple save files. On a recent update of this game, I realized that the trackers I used to note the items I collected before were super outdated, so I thought, "Hey, ik a thing or two about coding. Maybe I should make my own." This project is still a huge WIP, but I hope to complete it before I finish my 4th playthrough of this game lol
