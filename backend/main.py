from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from data.generator import *

app = FastAPI()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
