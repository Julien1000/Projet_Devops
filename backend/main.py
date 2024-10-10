from fastapi import FastAPI, Request, Form , APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import pandas as pd
from data.generator import *

from api_spotify.api import *
import csv
from pymongo import MongoClient
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
router = APIRouter(prefix="/api/v1")

templates = Jinja2Templates(directory="templates")
#app.mount("/static", StaticFiles(directory="static"), name="static")

# URI de connexion avec authentification

client = MongoClient(f'mongodb://admin:admin@mongodb:27017/')

db = client['devOpsBDD']  # Remplacez par le nom de votre base de données
collection = db['SpotifySongs']

all_songs = list(collection.find())
all_songs = clean_spotify_data_mongo(all_songs)


# df0=pd.read_csv('./data/spotify_data.csv')
# print(df0.iloc[14])

# print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§')
# print(all_songs.iloc[0])
# print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§')





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
@router.get("/prout")
async def read_item():
    return {"message": "Hello World"}

@router.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, query: Optional[str] = Form(None)):
    input_song = all_songs[all_songs['trackName'].notna() & all_songs['trackName'].str.contains(query, case=False)].iloc[0]
    playlist = generate_playlist(all_songs, input_song, 10)
    playlist = playlist[1:10]  
    # Passer la playlist au template HTML

    return templates.TemplateResponse("predict.html", {"request": request, "playlist": playlist})

@router.post("/get_track_infos")
async def predict(request: Request, track_id: str = Form(...)):
    infos_track = get_audio_features(track_id)
    
    features = list(infos_track.keys())
    
    playlist = generate_playlist(collection, infos_track, 9, features)
    return {"message": playlist}

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
