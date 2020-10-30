import spotipy
from .models import Category, TopSongs, TopGenres, TopArtists
from .import db
from flask import Blueprint
import requests
import json
from sqlalchemy import update

class SongData:
    def __init__(self):
        if Category.query.count() < 1:
            self.init_categories()

    def init_categories(self):
        short_term = Category(id='short-term')
        medium_term = Category(id='medium-term')
        long_term = Category(id='long-term')
        recent = Category(id='recent')
        saved = Category(id='saved')
        db.session.add_all([short_term, medium_term, long_term, saved, recent])
        db.session.commit()

    def get_top_songs(self, time, header, url):
        user_top_songs = "{}/me/top/tracks?limit=50&time_range={}".format(url, time)
        top_response = requests.get(user_top_songs, headers=header)
        top_data = json.loads(top_response.text)
        return top_data
    
    def set_recently_played(self, header, url, num):
        count = num
        user_recent = "{}/me/player/recently-played?type=track&limit=50".format(url)
        top_response = requests.get(user_recent, headers=header)
        results = json.loads(top_response.text)
        songs = []
        for song in results['items']:
            song = song['track']
            add_song = TopSongs(id = count, uri=song['uri'], title=song['name'], album=song['album']['name'],
                             artist=song['artists'][0]['name'], popularity=song['popularity'], 
                             artist_href=song['artists'][0]['href'], album_href=song['album']['href'], term='recent')
            album = requests.get(song['album']['href'], headers=header)
            album = json.loads(album.text)
            album_img = album['images'][0]['url']
            add_song.img = album_img
            songs.append(add_song)
            count = count + 1
        db.session.add_all(songs)
        db.session.commit()
    
    def set_top_songs(self, data, time, num, header):
        count = num
        songs = []
        results = data
        for song in results['items']:
            add_song = TopSongs(id = count, uri=song['uri'], title=song['name'], album=song['album']['name'],
                             artist=song['artists'][0]['name'], popularity=song['popularity'], 
                             artist_href=song['artists'][0]['href'], album_href=song['album']['href'], term=time)
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

    def set_saved_songs(self, data, header, num):
        count = num
        songs = []
        results = data
        for song in results:
            date = song['added_at']
            song = song['track']
            add_song = TopSongs(id = count, date=date, uri=song['uri'], title=song['name'], album=song['album']['name'],
                        artist=song['artists'][0]['name'], popularity=song['popularity'], 
                        artist_href=song['artists'][0]['href'], album_href=song['album']['href'], term='saved')
            songs.append(add_song)
            count = count + 1
        db.session.add_all(songs)
        db.session.commit()

    def set_top_genres(self, header):
        list_dict = {'short_term': [], 'medium_term': [], 'long_term': [], 'saved':[], 'recent': []}
        songs = db.session.query(TopSongs).all()
        print('setting genres')
        i = 1
        for song in songs:
            ref = song.artist_href
            term = song.term
            request = json.loads((requests.get(ref, headers=header)).text)
            genres = request['genres']
            for genre in genres:
                list_dict[term].append(genre)
            i = i + 1
        
        genres = []
        count = 1
        for key in list_dict:
            counts = []
            listt = list_dict[key]
            #calculate counts for each genre and get top 20
            no_repeats = set(listt)
            for item in no_repeats:
                counts.append(listt.count(item))
            tup = list(zip(no_repeats, counts))
            clean = sorted(tup, key=lambda x: x[1], reverse=True)
            top_clean = clean[0:20]
            #put into genres model
            j = 1
            for genre in top_clean:
                print("setting genre {}", j)
                genre_mod = TopGenres(id = count, name = genre[0], count=genre[1], term=key)
                genres.append(genre_mod)
                count = count + 1
                j = j  + 1
        db.session.add_all(genres)
        db.session.commit()

    def set_database(self, header, url):
        ##set top songs
        times = ['short_term', 'medium_term', 'long_term']
        num = 0
        for time in times:
            data = self.get_top_songs(time, header, url)
            self.set_top_songs(data, time, num, header)
            num = num + 50
        print("top set")
        self.set_recently_played(header, url, num)
        num = num + 50
        print('recent set')
        
        ##set saved songs
        data = self.get_saved_songs(header, url)
        self.set_saved_songs(data, header, num)
        print('saved set')
        
            

    def set_song_attrs(self, header, songs):
        ids = []
        for song in songs:
            song_id = (song['uri']).split(":")[2]
            ids.append(song_id)
        ids_str = ','.join(ids)   
        ref = 'https://api.spotify.com/v1/audio-features?ids={}'.format(ids_str)
        request = json.loads((requests.get(ref, headers=header)).text)
        return(request)
    
    def set_top_artists(self, header):
        list_dict = {'short_term': [], 'medium_term': [], 'long_term': [], 'saved':[], 'recent':[]}
        songs = db.session.query(TopSongs).all()
        print('setting artists')
        for song in songs:
            artist = song.artist
            term = song.term
            list_dict[term].append(artist)
        
        artists = []
        count = 1
        for key in list_dict:
            counts = []
            listt = list_dict[key]
            #calculate counts for each artist and get top 20
            no_repeats = set(listt)
            for item in no_repeats:
                counts.append(listt.count(item))
            tup = list(zip(no_repeats, counts))
            clean = sorted(tup, key=lambda x: x[1], reverse=True)
            top_clean = clean[0:20]
            #put into artists model
            j = 1
            for artist in top_clean:
                print("setting artist {}", j)
                artist_mod = TopArtists(id = count, name = artist[0], count=artist[1], term=key)
                artists.append(artist_mod)
                count = count + 1
                j = j  + 1
        db.session.add_all(artists)
        db.session.commit()

        


        
    
        


