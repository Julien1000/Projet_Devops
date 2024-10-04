from dotenv import load_dotenv
import base64
import os
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = post(url, headers=headers, data=data) 
    response_json = json.loads(response.content)
    token = response_json["access_token"]
    
    return token

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def get_artist_id(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1&market=FR"
    
    query_url = url + query
    response = get(query_url, headers=headers)
    
    if response.status_code == 200:
        response_json = json.loads(response.content)
        if response_json['artists']['items']:
            return response_json['artists']['items'][0]['id']
        else:
            print("Artiste non trouvé.")
            return None
    else:
        print(f"Erreur {response.status_code}: {response.content}")
        return None

def get_artist_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=FR"
    headers = get_auth_header(token)
    
    response = get(url, headers=headers)
    
    if response.status_code == 200:
        response_json = json.loads(response.content)
        return response_json['tracks'][:5]
    else:
        print(f"Erreur {response.status_code}: {response.content}")
        return None
    
def get_artist_genres(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    
    response = get(url, headers=headers)
    
    if response.status_code == 200:
        response_json = json.loads(response.content)
        return response_json['genres']
    else:
        print(f"Erreur {response.status_code}: {response.content}")
        return None

def search_by_track(token, track, market="FR"):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=track:{track}&type=track&limit=5&market={market}"
    
    query_url = url + query
    response = get(query_url, headers=headers)
    
    if response.status_code == 200:
        response_json = json.loads(response.content)
        tracks = response_json['tracks']['items']
        for track in tracks:
            print(f"- {track['name']}, (Artiste: {track['artists'][0]['name']}) (Popularité: {track['popularity']})")
        return tracks
    else:
        print(f"Erreur {response.status_code}: {response.content}")

def search_by_artist(token, artist):
    artist_id = get_artist_id(token, artist)
    if artist_id:
        tracks = get_artist_tracks(token, artist_id)
        if tracks:
            print(f"Top tracks de {artist}:")
            for track in tracks:
                print(f"- {track['name']} (Popularité: {track['popularity']})")
            return tracks
    else:    
        print("Artiste non trouvé.")

def search_by_track_and_artist(token, track, artist, market="FR"):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=track:{track} artist:{artist}&type=track&limit=5&market={market}"
    
    query_url = url + query
    response = get(query_url, headers=headers)
    
    if response.status_code == 200:
        response_json = json.loads(response.content)
        tracks = response_json['tracks']['items']
        for track in tracks:
            print(f"- {track['name']}, (Artiste: {track['artists'][0]['name']}) (Popularité: {track['popularity']})")
        return tracks
    else:
        print(f"Erreur {response.status_code}: {response.content}")

token = get_token()
tracks = search_by_track_and_artist(token, track='0 to 100', artist='Sidhu Moose Wala', market="US")

if tracks:
    track = tracks[0]
    track_id = track['id']

    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    response = get(url, headers=headers)

    if response.status_code == 200:
        response_json = json.loads(response.content)
    
        print(f"trackName: {track['name']}")
        print(f"artistName: {track['artists'][0]['name']}")
        print(f"msPlayed: {track['duration_ms']}")
        print(f"genre: {', '.join(get_artist_genres(token, track['artists'][0]['id']))}")
        print(f"danceability: {response_json['danceability']}")
        print(f"energy: {response_json['energy']}")
        print(f"key: {response_json['key']}")
        print(f"loudness: {response_json['loudness']}")
        print(f"mode: {response_json['mode']}")
        print(f"speechiness: {response_json['speechiness']}")
        print(f"acousticness: {response_json['acousticness']}")
        print(f"instrumentalness: {response_json['instrumentalness']}")
        print(f"liveness: {response_json['liveness']}")
        print(f"valence: {response_json['valence']}")
        print(f"tempo: {response_json['tempo']}")
        print(f"id: {response_json['id']}")
        print(f"uri: {response_json['uri']}")
        print(f"track_href: {response_json['track_href']}")
        print(f"analysis_url: {response_json['analysis_url']}")
        print(f"duration_ms: {response_json['duration_ms']}")
        print(f"time_signature: {response_json['time_signature']}")
