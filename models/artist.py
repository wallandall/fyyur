from flask.globals import session
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

    @classmethod
    def show_artist(cls, artist_id):
        artist = Artist.query.get(artist_id)

        data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website_link": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": True if artist.seeking_venue in (True, 't', 'True') else False,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link if artist.image_link else "",
            "past_shows": [],  # add a class function
            "upcomming_shows": [],  # zadd a class function
            "past_shows_count": 5,  # zadd a class function
            "upcomming_shows_count": 6  # zadd a class function

        }

        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update_artist(cls, form_data, artist_id):
        updated_artist = cls.query.get(artist_id)

        try:

            updated_artist.name = form_data.name.data
            updated_artist.genres = ','.join(
                str(e)for e in form_data.genres.data)
            updated_artist.state = form_data.state.data
            updated_artist.phone = form_data.phone.data
            updated_artist.website = form_data.website_link.data
            updated_artist.facebook_link = form_data.facebook_link.data
            updated_artist.city = form_data.city.data
            updated_artist.seeking_venue = True if form_data.seeking_venue.data in (
                True, 't', 'True') else False
            updated_artist.seeking_description = form_data.seeking_description.data
            updated_artist.image_link = form_data.image_link.data if form_data.image_link.data else ""

            db.session.commit()
            error = False

        except Exception as e:
            db.session.rollback()
            return False

        return True
