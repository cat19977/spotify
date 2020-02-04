import json
from flask import Flask, request, redirect, g, render_template, Blueprint, jsonify
import requests
from urllib.parse import quote
from .songs import SongData
from .models import Token, TopSongs, SavedSongs
from . import db
import ast

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

main = Blueprint('main', __name__)
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
SET_TOP_POST_URI = "{}:{}/set-top-songs".format(CLIENT_SIDE_URL, PORT)

#gets token from react and saves
@main.route('/add_token', methods=['GET','POST'])
def add_token():
    if request.method == 'POST':
        token = request.get_data()
        token = token.decode('utf-8')
        token_dict = json.loads(token) #consverts string dict to real dict
        access_token = token_dict['token']
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        header = json.dumps(authorization_header)
        #send token to database
        if Token.query.count()<1:
            send_token = Token(header = header, url = SPOTIFY_API_URL)
            db.session.add(send_token)
            db.session.commit()
        
        return redirect(SET_TOP_POST_URI)
    else:
        token = Token.query.count()
        print(token)
        if token > 0:
            return jsonify({"token":'true'})
        else:
            return jsonify({"token":'false'})

#gets top songs and stores them in database
@main.route('/set-top-songs', methods=['GET'])
def set_top_songs():
    header = Token.query.first().header
    url = Token.query.first().url
    header = ast.literal_eval(header)
    songs = SongData()
    times = ['short_term', 'medium_term', 'long_term']
    num = 0
    for time in times:
        data = songs.get_top_songs(time, header, url)
        if TopSongs.query.count() < 150:
            songs.set_top_songs(data, time, num, header)
        num = num + 50
    return jsonify({'success':'yes'})

@main.route('/get-top-songs', methods=['GET'])
def get_top_songs():
    songs = TopSongs.query.all()
    s = jsonify({'data': [song.serialize for song in songs]})
    return s

@main.route('/set-saved-songs', methods=['GET'])
def set_saved_songs():
    header = Token.query.first().header
    url = Token.query.first().url
    header = ast.literal_eval(header)
    songs = SongData()
    data = songs.get_saved_songs(header, url)
    if SavedSongs.query.count() == 0:
        songs.set_saved_songs(data, header)
    return jsonify({'success':'yes'})

@main.route('/get-saved-songs', methods=['GET'])
def get_saved_songs():
    songs = SavedSongs.query.all()
    s = jsonify({'data': [song.serialize for song in songs]})
    return s

