from fastapi import FastAPI, Request, Form , APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import pandas as pd
from data.generator import *

from api_spotify.api import *
from pymongo import MongoClient


app = FastAPI()


app = FastAPI()
router = APIRouter(prefix="/api/v1")
# Charger et nettoyer les données Spotify
df = pd.read_csv('./data/spotify_data.csv')
df = clean_spotify_data_csv(df)

client = MongoClient("mongodb://admin:admin@mongodb:27017/")
db = client["DevOpsDB"]
collection = db["SpotifySongs"]
# Configuration des templates
templates = Jinja2Templates(directory="templates")

# Endpoint pour générer la playlist
@router.post("/predict")
async def predict(request: Request, query: Optional[str] = Form(None)):
    # Filtrer la chanson entrée par l'utilisateur dans le dataset
    token = get_token()
    tracks = search_by_track(query)
    
    return templates.TemplateResponse("search.html", {"request": request, "tracks": tracks})
    return {"message":input_song}
    # Vérifier si la chanson existe dans les données
    if input_song.empty:
        
       
        return templates.TemplateResponse("predict.html", {"request": request, "error": "Chanson non trouvée"})

    # Générer une playlist basée sur la chanson d'entrée
    playlist = generate_playlist(df, input_song, 9)
    
    # Envoyer la playlist au front-end
    return templates.TemplateResponse("predict.html", {"request": request, "playlist": playlist})

@router.post("/get_track_infos")
async def predict(request: Request, track_id: str = Form(...)):
    infos_track = get_audio_features(track_id)
    features = infos_track.keys()
    playlist = generate_playlist(df, infos_track, 9, features)
    # return templates.TemplateResponse("predict.html", {"request": request, "playlist": playlist})
    keys = infos_track.keys()

    # Afficher les clés
    print(keys)
    return {"message:": infos_track}

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
