from fastapi import FastAPI, Request, Form , APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import pandas as pd
from data.generator import *
import csv
from pymongo import MongoClient

app = FastAPI()
router = APIRouter(prefix="/api/v1")

username = 'Marco'  # Remplacez par votre nom d'utilisateur MongoDB
password = 'jojopause123'     # Remplacez par votre mot de passe MongoDB
host = 'localhost'                  # Remplacez par l'hôte de votre MongoDB, par ex. localhost ou IP distante
port = '27017'                      # Remplacez par le port (habituellement 27017 par défaut)
db_name = 'Database_spotify'           # Remplacez par le nom de votre base de données

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





# Configuration des templates
templates = Jinja2Templates(directory="templates")

@router.get("/prout")
async def read_item():
    return {"message": "Hello World"}

# Endpoint pour générer la playlist
@router.post("/predict")
async def predict( query: Optional[str] = Form(None)):
    
    # Filtrer la chanson entrée par l'utilisateur dans le dataset
    # Utilisation de la regex pour faire une recherche insensible à la casse dans MongoDB
    # input_song = collection.find_one({"trackName": {"$regex": query, "$options": "i"}})
    input_song = all_songs[all_songs['trackName'].str.contains(query, case=False)].iloc[0]
    
# Affichage du premier résultat
    if input_song:
        print(input_song)
    else:
        print("Aucun résultat trouvé.")
    
    
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    playlist = generate_playlist(all_songs, input_song, 9)
    print(playlist)
    print("////////////////////////////////////////////////////////////////////////////////////////////////")

    return {"message"}
    # Vérifier si la chanson existe dans les données
   

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
