from . import db

class Token(db.Model):
    __table_args__ = {'extend_existing': True} 
    url = db.Column(db.String(100), primary_key=True)
    header = db.Column(db.String(500))

class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.String(50), primary_key=True)
    songs = db.relationship('TopSongs')

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
    category_id = db.Column(db.String(50), db.ForeignKey('categories.id'))
    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {'id': self.id,
                'title': self.title,
                'artist': self.artist,
                'album': self.album,
                'popularity': self.popularity,
                'term': self.category_id,
                'artist_href': self.artist_href,
                'album_href': self.album_href,
                'img': self.img
        }

class SavedSongs(db.Model):
    __tablename__ = 'saved_songs'
    __table_args__ = {'extend_existing': False}
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(50))
    title = db.Column(db.String(50))
    artist = db.Column(db.String(50))
    album = db.Column(db.String(50))
    popularity = db.Column(db.Integer)
    category_id = db.Column(db.String(50), db.ForeignKey('categories.id'))

