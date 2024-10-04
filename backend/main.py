<<<<<<< HEAD
from fastapi import FastAPI, Request, Form
=======
from fastapi import FastAPI, Request , APIRouter ,Form
>>>>>>> e34df1f6ad31159d37ece6a99e3e14c629243862
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import pandas as pd
from data.generator import *

app = FastAPI()
<<<<<<< HEAD

# Charger et nettoyer les données Spotify
df = pd.read_csv('/home/cytech/Desktop/cours_dev_ops/Projet_Devops/backend/data/spotify_data.csv')
df = clean_spotify_data_csv(df)

# Configuration des templates
templates = Jinja2Templates(directory="templates")

# Endpoint pour générer la playlist
@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, query: str = Form(...)):
    # Filtrer la chanson entrée par l'utilisateur dans le dataset
    input_song = df[df['trackName'].str.contains(query, case=False)].iloc[0]
    
    
    
    
    
    # Vérifier si la chanson existe dans les données
    if input_song.empty:
       
        return templates.TemplateResponse("predict.html", {"request": request, "error": "Chanson non trouvée"})

    # Générer une playlist basée sur la chanson d'entrée
    playlist = generate_playlist(df, input_song, 9)
    
    # Envoyer la playlist au front-end
    return templates.TemplateResponse("predict.html", {"request": request, "playlist": playlist})
=======
router = APIRouter(prefix="/api/v1")
# Configuration des templates
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root():
    return {"message": "Hello, CACA Song Attributes!"}

@router.get("/data", response_class=HTMLResponse)
async def get_data(request: Request):
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv('./data/spotify_data.csv')  # Ajuster le chemin si nécessaire

    # Convertir le DataFrame en HTML
    table_html = df.to_html(classes='table table-striped')
    # Rendre le template avec la table
    return templates.TemplateResponse("index.html", {"request": request, "table": table_html})
>>>>>>> e34df1f6ad31159d37ece6a99e3e14c629243862

@router.post("/predict")
async def predict(query: Optional[str] = Form(None)):
    return {"query": query}

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
