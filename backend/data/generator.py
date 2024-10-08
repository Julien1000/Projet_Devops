import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors



def clean_spotify_data_mongo(mongo_data, features=['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']):
    # Convert MongoDB data to DataFrame
    df = pd.DataFrame(list(mongo_data))

    # Replace NaN genres with 'Inconnu'
    df['genre'].fillna('Inconnu', inplace=True)

    # Drop rows with missing data
    df.dropna(inplace=True)

    # Remove duplicate tracks based on 'id'
    df.drop_duplicates(subset="id", inplace=True)

    # Standardize the audio features
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])
  
    return df




def generate_playlist(data_source,input_song,K,features=['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']):

    nn = NearestNeighbors(n_neighbors=K,algorithm="ball_tree")
    nn.fit(data_source[features])

    scaler = StandardScaler()
    #input_song[features] = scaler.fit_transform(input_song[features])
    input_data = [input_song[features]]

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

