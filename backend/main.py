import re
from fastapi import FastAPI, Request, Form , APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from data.generator import *

from api_spotify.api import *

from pymongo import MongoClient
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from requests import post, get
import json
import os

app = FastAPI()
router = APIRouter(prefix="/api/v1")

templates = Jinja2Templates(directory="templates")
#app.mount("/static", StaticFiles(directory="static"), name="static")

# URI de connexion avec authentification

#mongo_connection_string = os.environ["mongo_uri"]
mongo_connection_string = "mongodb://admin:admin@mongodb:27017/"
client = MongoClient(mongo_connection_string)

db = client['DevOpsDB']  # Remplacez par le nom de votre base de données
collection = db['SpotifySongs']



all_songs = list(collection.find())
all_songs, scaler , features = clean_spotify_data_mongo(all_songs)


# df0=pd.read_csv('./data/spotify_data.csv')
# print(df0.iloc[14])

# print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§')
# print(all_songs.iloc[0])
# print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§')
def parse_request(user_query):
    artist_regex = re.compile(r'artist:\"([^\"]+)\"', re.IGNORECASE)
    artist_match = artist_regex.search(user_query)
    
    track_name_query = user_query
    artist_name = None
    
    if artist_match:
        artist_name = artist_match.group(1)
        track_name_query = artist_regex.sub('', user_query).strip()
    
    return track_name_query.strip(), artist_name

def fetc_img(id):
    url = f"https://embed.spotify.com/oembed?url=https://open.spotify.com/track/{id}"
    response = get(url)
    if response.status_code == 200:
        response_json = json.loads(response.content)    
        return response_json['thumbnail_url']
    

def search_in_db(track_name,artist_name):
    query = {}
    if track_name:
       query["trackName"] = {"$regex": track_name, "$options": "i"}

    if artist_name:
        query["artistName"] = artist_name
    
    res = collection.find_one(query)
    return res


client = MongoClient("mongodb://admin:admin@mongodb:27017/")
db = client["devOpsBDD"]
collection = db["SpotifySongs"]
# Configuration des templates
templates = Jinja2Templates(directory="templates")

@router.get("/random")
async def random(request: Request,):
    input_song =all_songs.sample(n=1).iloc[0]
    img_uri = fetc_img(input_song.id)
    playlist = generate_playlist(all_songs, input_song, 10)
    playlist = playlist[1:10]  

    return templates.TemplateResponse("out.html", {"request": request , "playlist": playlist , "input_song":input_song , "image": img_uri})



# Endpoint pour générer la playlist
@router.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, query: Optional[str] = Form(None)):
    q = parse_request(query)
    item = search_in_db(q[0],q[1])
    item = pd.DataFrame([item])
    item[features] = scaler.transform(item[features])
    #filtered_songs = all_songs[all_songs['trackName'].notna() & all_songs['trackName'].str.contains(query, case=False)]
    filtered_songs = item

    if not filtered_songs.empty:
        input_song = filtered_songs.iloc[0]
        img_uri = fetc_img(input_song.id)
        playlist = generate_playlist(all_songs, input_song, 10)
        playlist = playlist[1:10]  
        return templates.TemplateResponse("out.html", {"request": request, "playlist": playlist , "input_song":input_song , "image": img_uri})
    else:
        tracks = search_by_track(query)
        return templates.TemplateResponse("search.html", {"request": request, "tracks": tracks})
    
@router.post("/get_track_infos")
async def predict(request: Request, track_id: str = Form(...)):
    audio_features = get_audio_features(track_id)
    input_song = get_infos_track(track_id)
    img_uri = fetc_img(track_id)
    features = list(audio_features.keys())
    playlist = generate_playlist(all_songs, audio_features, 9, features)
    
    return templates.TemplateResponse("out.html", {"request": request, "playlist": playlist , "input_song":input_song , "image": img_uri})

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
