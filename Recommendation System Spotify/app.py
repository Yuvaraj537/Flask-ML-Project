from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector

app = Flask(__name__)

# Load your dataset
df = pd.read_csv("Clusterd_df.xls")

numerical_features = [
    "valence", "danceability", "energy", "tempo",
    "acousticness", "liveness", "speechiness", "instrumentalness"
]

# Spotify API credentials
SPOTIFY_CLIENT_ID = '86dfb8a0b364401fab44200b21b3e00b'
SPOTIFY_CLIENT_SECRET = 'aaa75850ff394ef5bb14485fa99dd894'

# Setup Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="musicdb"
)
cursor = db.cursor()

# Get Spotify info for a song
def get_spotify_info(song_name):
    try:
        result = sp.search(q=song_name, limit=1, type='track')
        if result["tracks"]["items"]:
            track = result["tracks"]["items"][0]
            return {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "image": track["album"]["images"][0]["url"],
                "url": track["external_urls"]["spotify"]
            }
    except:
        return None

# Recommendation logic
def recommend_songs(song_name, df, num_recommendations=5):
    if song_name not in df['name'].values:
        raise ValueError("Song not found in dataset.")

    song_cluster = df[df["name"] == song_name]["Cluster"].values[0]
    same_cluster_songs = df[df["Cluster"] == song_cluster]

    song_index = same_cluster_songs[same_cluster_songs['name'] == song_name].index[0]
    cluster_features = same_cluster_songs[numerical_features]

    similarity = cosine_similarity(cluster_features)
    similarity_scores = similarity[same_cluster_songs.index.get_loc(song_index)]
    similar_indices = similarity_scores.argsort()[-(num_recommendations + 1):-1][::-1]

    recommendations = same_cluster_songs.iloc[similar_indices][["name", "year", "artists"]]
    return recommendations

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Handle recommendations
@app.route("/recommend", methods=["POST"])
def recommend():
    recommendations = []
    if request.method == "POST":
        song_name = request.form.get("song_name")
        try:
            recommendations_df = recommend_songs(song_name, df)
            for _, row in recommendations_df.iterrows():
                info = get_spotify_info(row['name'])
                if info:
                    recommendations.append({
                        "name": row['name'],
                        "artists": row['artists'],
                        "year": row['year'],
                        "spotify_url": info["url"],
                        "image_url": info["image"]
                    })
        except Exception as e:
            recommendations = [{"name": "Error", "artists": str(e), "year": ""}]
    return render_template("index.html", recommendations=recommendations)

# Song details and save to DB
@app.route("/song")
def show_song():
    song_name = request.args.get("song_name")
    info = get_spotify_info(song_name)
    if info:
        # Save to database
        query = """
        INSERT INTO recommended_songs (input_song, recommended_song, artist, year)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (song_name, info["name"], info["artist"], 0))
        db.commit()

        return render_template("song.html", song=info)
    else:
        return "Spotify info not found."
    
if __name__ == "__main__":
    app.run(debug=True)
    

