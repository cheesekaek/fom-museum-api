## fom-museum-api
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
