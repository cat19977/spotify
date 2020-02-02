import json
from flask import Flask, request, redirect, g, render_template, Blueprint, jsonify
import requests
from urllib.parse import quote
from .songs import SongData
from .models import Token
from . import db
import ast

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

main = Blueprint('main', __name__)

class Login:
    CLIENT_ID = "d9dca95c2ee54a54b35c890972268f0a"
    CLIENT_SECRET = "4b426805943844efbc248fd10663aaab"
    #spotify urls
    SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_API_BASE_URL = "https://api.spotify.com"
    API_VERSION = "v1"
    SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
    # Server-side Parameters
    CLIENT_SIDE_URL = "http://127.0.0.1"
    PORT = 5000
    REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
    POST_URI = "{}:{}/top-songs".format(CLIENT_SIDE_URL, PORT)
    SCOPE = 'user-top-read'
    STATE = ""
    SHOW_DIALOG_bool = True
    SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "client_id": CLIENT_ID
    }
        
    @main.route("/")
    def index():
        # Auth Step 1: Authorization
        url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in Login.auth_query_parameters.items()])
        auth_url = "{}/?{}".format(Login.SPOTIFY_AUTH_URL, url_args)
        return redirect(auth_url)


    @main.route("/callback/q")
    def callback():
        # Auth Step 4: Requests refresh and access tokens
        auth_token = request.args['code']
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": Login.REDIRECT_URI,
            'client_id': Login.CLIENT_ID,
            'client_secret': Login.CLIENT_SECRET,
        }
        post_request = requests.post(Login.SPOTIFY_TOKEN_URL, data=code_payload)

        # Auth Step 5: Tokens are Returned to Application
        response_data = json.loads(post_request.text)
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
        token_type = response_data["token_type"]
        expires_in = response_data["expires_in"]

        # Auth Step 6: Use the access token to access Spotify API
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        
        ##send data to database
        token = Token(url = Login.SPOTIFY_API_URL, header = json.dumps(authorization_header))
        db.session.add(token)
        db.session.commit()

        
        return redirect(Login.POST_URI)


@main.route('/top-songs', methods=['GET'])
def top_songs():
    header = Token.query.first().header
    url = Token.query.first().url
    header = ast.literal_eval(header)
    songs = SongData()
    times = ['short_term', 'medium_term', 'long_term']
    num = 0
    for time in times:
        data = songs.get_top_songs(time, header, url)
        songs.set_top_songs(data, time, num)
        num = num + 50
    return jsonify({'success':'yes'})

@main.route('/saved-songs', methods=['GET'])
def saved_songs():
    return jsonify({'success':'yes'})

    
