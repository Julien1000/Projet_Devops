from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

app = FastAPI()

# Configuration des templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root():
    return {"message": "Hello, Spotify Song Attributes!"}

@app.get("/data", response_class=HTMLResponse)
async def get_data(request: Request):
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv('Spotify_Song_Attributes.csv')  # Ajuster le chemin si nécessaire

    # Convertir le DataFrame en HTML
    table_html = df.to_html(classes='table table-striped')

    # Rendre le template avec la table
    return templates.TemplateResponse("index.html", {"request": request, "table": table_html})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

