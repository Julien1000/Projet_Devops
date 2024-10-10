import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

def clean_spotify_data_csv(df, features=['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']):
    #changement des genres non connus à inconnu 
    df['genre'].fillna('Inconnu', inplace=True)
    #suppression des lignes avec des données vides
    df.dropna(inplace=True)
    #suppresion des titres en doublons
    df.drop_duplicates(subset="id",inplace=True)

    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])

    return df


def generate_playlist(data_source,input_song,K,features=['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']):
    nn = NearestNeighbors(n_neighbors=K,algorithm="ball_tree")
    nn.fit(data_source[features])

    scaler = StandardScaler()
    #input_song[features] = scaler.fit_transform(input_song[features])
    
    input_data = [[input_song[feature] for feature in features]]

    distances, indices = nn.kneighbors(input_data)

    output = []
    for dist,indice in zip(distances[0] ,indices[0]):
        output.append({
            "song_name": data_source.iloc[indice]['trackName'],
            "artiste_name": data_source.iloc[indice]['artistName'],
            "song_genre" : data_source.iloc[indice]['genre'],
            "song_distance": dist
        })
    return output
