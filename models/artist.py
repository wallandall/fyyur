from db import db


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    image_link = db.Column(db.String(500))

    def __init__(self, name, genres, city, state, phone, website, facebook_link, seeking_venue, seeking_description, image_link):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.image_link = image_link

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def list_artis(cls):
        data = []
        artist = Artist.query.with_entities(
            Artist.id, Artist.name).distinct().all()
        for a in artist:
            artist_id = a.id
            name = a.name
            data.append({
                "id": artist_id,
                "name": name,
            })
        return data

    @classmethod
    def find_artist(cls, name):
        artists = cls.query.filter(cls.name.ilike('%' + name + '%'))
        data = []
        for artist in artists:
            data.append({
                "id": artist.id,
                "name": artist.name,

            })
        count = len(data)
        response = {
            "count": count,
            "data": data
        }

        return response
