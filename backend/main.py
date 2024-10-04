from fastapi import FastAPI, Request, Form , APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import pandas as pd
from data.generator import *

app = FastAPI()
router = APIRouter(prefix="/api/v1")
# Charger et nettoyer les données Spotify
df = pd.read_csv('./data/spotify_data.csv')
df = clean_spotify_data_csv(df)

# Configuration des templates
templates = Jinja2Templates(directory="templates")

@router.get("/prout")
async def read_item():
    return {"message": "Hello World"}

# Endpoint pour générer la playlist
@router.post("/predict")
async def predict( query: Optional[str] = Form(None)):
    
    # Filtrer la chanson entrée par l'utilisateur dans le dataset
    input_song = df[df['trackName'].str.contains(query, case=False)].iloc[0]
    playlist = generate_playlist(df, input_song, 9)

    print(playlist)
    return {"message":query}
    return {"message":input_song}
    # Vérifier si la chanson existe dans les données
    if input_song.empty:
       
        return templates.TemplateResponse("predict.html", {"request": request, "error": "Chanson non trouvée"})

    # Générer une playlist basée sur la chanson d'entrée
    playlist = generate_playlist(df, input_song, 9)
    
    # Envoyer la playlist au front-end
    return templates.TemplateResponse("predict.html", {"request": request, "playlist": playlist})

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
