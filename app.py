from flask import Flask, render_template, send_from_directory, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import requests
from producer import send_song_data
import json
from flask import jsonify
import time


client = MongoClient("mongodb://localhost:27017/")
db = client.BDA_Project
collection = db.songs_meta_data

app = Flask(__name__)

LASTFM_API_KEY = '31fe3d279288de0a7f8997ffb8cba2ab'

def get_album_art(artist, album):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "album.getinfo",
        "api_key": LASTFM_API_KEY,
        "artist": artist,
        "album": album,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200 and 'album' in data:
        return data['album'].get('image', [{}])[-1].get('#text')  # Get the largest image
    else:
        return url_for('static', filename='default.jpg')

def load_audio_metadata():
    audio_files = []
    for item in collection.find():
        audio_files.append(item)
    return audio_files

audio_files = load_audio_metadata()

@app.route('/audio/<path:filename>')
def send_audio(filename):
    # Convert backslashes to forward slashes
    filename = filename.replace('\\', '/')
    # directory = r'D:\University\Semester 4\BIG DATA\project'
    directory = r'/home/hdoop/Documents/project/'
    full_path = os.path.join(directory, filename)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")  # Debug output
        return "File not found", 404
    return send_from_directory(directory, filename, as_attachment=False)


@app.route('/')
def home():
    return render_template('index.html', audio_files=audio_files)


@app.route('/song/<song_id>')
def song_details(song_id):
    
    song = collection.find_one({'_id': ObjectId(song_id)})
    album_art_url = get_album_art(song['artist'], song['album'])
    song_path = song['path']
    song_number = int(song_path[15:20:1])
    send_song_data(song_number)

    start_time = time.time()
    timeout = 20
    while time.time() - start_time < timeout:
        try:
            with open('recommended_songs.json', 'r') as json_file:
                similar_songs = json.load(json_file)
            if similar_songs.get('song_id') == song_number:
                break
        except (IOError, ValueError, KeyError):
            pass
        time.sleep(1)
    else:
        return 'Recommendation processing timeout.', 503
    
    similar_songs_path = similar_songs.get('path')

    print(similar_songs_path)
    similar_songs_cursor = collection.find({"path": {"$in": similar_songs_path}})
    similar_songs_list = list(similar_songs_cursor)
    similar_songs_dict = {song['path']: song for song in similar_songs_list}
    ordered_similar_songs = [similar_songs_dict[path] for path in similar_songs_path if path in similar_songs_dict]

    if song:
        return render_template('song.html', song=song, album_art_url=album_art_url, similar_songs = ordered_similar_songs)
    else:
        return 'Song not found', 404

if __name__ == '__main__':
    app.run(debug=True)
