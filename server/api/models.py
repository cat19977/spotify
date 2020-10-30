from . import db

class Token(db.Model):
    __table_args__ = {'extend_existing': True} 
    url = db.Column(db.String(100), primary_key=True)
    header = db.Column(db.String(500))
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'url': self.url,
            'header': self.header,
        }
        
class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.String(50), primary_key=True)
    top_genres = db.Column(db.String(1024))
    songs = db.relationship('TopSongs')
    top_genres = db.relationship('TopGenres')
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'top_genres': self.top_genres,
        }

class TopSongs(db.Model):
    __tablename__ = 'songs'
    __table_args__ = {'extend_existing': False}
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(50))
    title = db.Column(db.String(50))
    artist = db.Column(db.String(50))
    album = db.Column(db.String(50))
    popularity = db.Column(db.Integer)
    artist_href = db.Column(db.String(50))
    album_href = db.Column(db.String(50))
    img = db.Column(db.String(50))
    term = db.Column(db.String(50), db.ForeignKey('categories.id'))
    date = db.Column(db.String(50))
    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {'id': self.id,
                'title': self.title,
                'artist': self.artist,
                'album': self.album,
                'uri': self.uri,
                'popularity': self.popularity,
                'term': self.term,
                'artist_href': self.artist_href,
                'album_href': self.album_href,
                'img': self.img,
                'date': self.date
        }

class TopGenres(db.Model):
    __tablename__ = 'genres'
    __table_args__ = {'extend_existing': False}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    count = db.Column(db.Integer)
    term = db.Column(db.String(50), db.ForeignKey('categories.id'))
    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {'id': self.id,
                'name': self.name,
                'count': self.count,
                'term': self.term
        }

class TopArtists(db.Model):
    __tablename__ = 'artists'
    __table_args__ = {'extend_existing': False}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    count = db.Column(db.Integer)
    term = db.Column(db.String(50), db.ForeignKey('categories.id'))
    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {'id': self.id,
                'name': self.name,
                'count': self.count,
                'term': self.term
        }










