import spotipy
from .models import Category, TopSongs, SavedSongs
from .import db
from flask import Blueprint
import requests
import json

class SongData:
    def __init__(self):
        if Category.query.count() < 1:
            self.init_categories()

    def init_categories(self):
        short_term = Category(id='short-term')
        medium_term = Category(id='medium-term')
        long_term = Category(id='long-term')
        db.session.add_all([short_term, medium_term, long_term])
        db.session.commit()

    def get_top_songs(self, time, header, url):
        user_top_songs = "{}/me/top/tracks?limit=50&time_range={}".format(url, time)
        top_response = requests.get(user_top_songs, headers=header)
        top_data = json.loads(top_response.text)
        return top_data
    
    def set_top_songs(self, data, time, num, header):
        count = num
        songs = []
        results = data
        for song in results['items']:
            add_song = TopSongs(id = count, uri=song['uri'], title=song['name'], album=song['album']['name'],
                             artist=song['artists'][0]['name'], popularity=song['popularity'], 
                             artist_href=song['artists'][0]['href'], album_href=song['album']['href'], category_id=time)
            album = requests.get(song['album']['href'], headers=header)
            album = json.loads(album.text)
            album_img = album['images'][0]['url']
            add_song.img = album_img
            songs.append(add_song)
            count = count + 1
        db.session.add_all(songs)
        db.session.commit()
    
    def get_saved_songs(self, header, url):
        results_pre = "{}/me/tracks?limit=50".format(url)
        results = json.loads((requests.get(results_pre, headers=header)).text)
        offset = 50
        result = results['items']
        diff = 125
        while diff >= 50:
            results_pre = "{}/me/tracks?limit=50&offset={}".format(url, offset)
            results = json.loads((requests.get(results_pre, headers=header)).text)
            for item in results['items']:
                result.append(item)
            diff = results['total'] - len(result)
            offset +=50
        new_pre = "{}/me/tracks?limit=50&offset={}&limit={}".format(url, offset, diff)
        new = json.loads((requests.get(new_pre, headers=header)).text)
        for item in new['items']:
            result.append(item)
        return result

    def set_saved_songs(self, data, header):
        count = 0
        songs = []
        results = data
        for song in results:
            song = song['track']
            add_song = SavedSongs(id = count, uri=song['uri'], title=song['name'], album=song['album']['name'],
                        artist=song['artists'][0]['name'], popularity=song['popularity'], 
                        artist_href=song['artists'][0]['href'], album_href=song['album']['href'])
            songs.append(add_song)
            count = count + 1
        db.session.add_all(songs)
        db.session.commit()
    
        


