import json
from flask import Flask, request, redirect, g, render_template, Blueprint, jsonify
import requests
from urllib.parse import quote
from .songs import SongData
from .models import Token, TopSongs, Category, TopGenres, TopArtists
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
SET_TOP_POST_URI = "{}:{}/set-database".format(CLIENT_SIDE_URL, PORT)

#gets token from react and saves
@main.route('/add_token', methods=['GET','POST'])
def add_token():
    if request.method == 'POST':
        api = SongData()
        token = request.get_data()
        token = token.decode('utf-8')
        token_dict = json.loads(token) #consverts string dict to real dict
        access_token = token_dict['token']
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        header = json.dumps(authorization_header)
        header_api = ast.literal_eval(header)
        #send token to database
        if Token.query.count()<1:
            send_token = Token(header = header, url = SPOTIFY_API_URL)
            db.session.add(send_token)
            db.session.commit()
        
        ##sets database info for songs
        api.set_database(header_api, SPOTIFY_API_URL)

        #sets database info genres
        api.set_top_genres(header_api)

        ##sets top artists
        api.set_top_artists(header_api)
        
        return jsonify({"success":'yes'})
    else:
        token = Token.query.count()
        if token == 0:
            return jsonify({"token":'false'})
        else:
            token = Token.query.first()
            return jsonify({"token":'true'})


@main.route('/get-songs', methods=['GET'])
def get_songs():
    term = request.args.get('term')
    songs = TopSongs.query.filter(TopSongs.term == term).all()
    s = jsonify({'data': [song.serialize for song in songs]})
    return s

@main.route('/get-genres', methods=['GET'])
def get_genres():
    term = request.args.get('term')
    genres = TopGenres.query.filter(TopGenres.term == term).all()
    s = jsonify({'data': [genre.serialize for genre in genres]})
    return s

@main.route('/get-artists', methods=['GET'])
def get_artists():
    term = request.args.get('term')
    artists = TopArtists.query.filter(TopArtists.term == term).all()
    s = jsonify({'data': [artist.serialize for artist in artists]})
    return s

@main.route('/get-song-attr', methods=['GET'])
def get_attr():
    term = request.args.get('term')
    header = Token.query.first().header
    header = ast.literal_eval(header)
    print(header)
    songs = TopSongs.query.filter(TopSongs.term == term).all()
    print(songs[0])
    s = [song.serialize for song in songs]
    api = SongData()
    attrs = api.set_song_attrs(header, s)
    return jsonify({'hi':attrs})
