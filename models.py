

from flask.globals import session
from sqlalchemy.orm import query
from sqlalchemy import UniqueConstraint, distinct

from datetime import datetime
from db import db


#############################################################################################################
##                                          Venue Model                                                   ##
#############################################################################################################


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String(120)))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue',
                            lazy=True, cascade='all, delete-orphan')
    UniqueConstraint('name', 'city', 'state', 'address',
                     name='unique_name_city_state_address')

    def __init__(self, name, genres, address, city, state, phone, website, facebook_link, seeking_talent, seeking_description, image_link):
        self.name = name
        self.genres = genres
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description
        self.image_link = image_link

    @property
    def upcoming_shows(self):
        upcoming_shows = [
            show for show in self.shows if show.start_time > datetime.now()]
        return upcoming_shows

    @property
    def num_upcoming_shows(self):
        return len(self.upcoming_shows)

    @property
    def past_shows(self):
        past_shows = [
            show for show in self.shows if show.start_time < datetime.now()]
        return past_shows

    @property
    def num_past_shows(self):
        return len(self.past_shows)

    @ classmethod
    def find_by_name(cls, search_term):
        venues = cls.query.filter(cls.name.ilike('%' + search_term + '%'))
        data = []
        for venue in venues:
            data.append({
                "id": venue.id,
                "name": venue.name,

            })
        count = len(data)
        response = {
            "count": count,
            "data": data
        }

        return response

    @ classmethod
    def venue_exists(cls, name):
        venue_exisits = cls.query.filter_by(name=name).first()
        if venue_exisits:
            return True
        else:
            return False

    @ classmethod
    def list_venue(cls):
        data = []
        city_state = cls.query.with_entities(
            cls.city, cls.state).distinct().all()
        for c in city_state:
            city = c[0]
            state = c[1]
            venues = cls.query.filter_by(city=city, state=state).all()
            shows = venues[0].upcoming_shows
            data.append({
                "city": city,
                "state": state,
                "venues": venues,
                "num_upcoming_shows": shows
            })
        return data

    @ classmethod
    def show_venue(cls, venue_id):
        venue = cls.query.get(venue_id)
        upcoming_shows = []
        past_shows = []
        if venue:
            data = {
                "id": venue.id,
                "name": venue.name,
                "genres": venue.genres,
                "address": venue.address,
                "city": venue.city,
                "state": venue.state,
                "phone": venue.phone,
                "website": venue.website,
                "facebook_link": venue.facebook_link,
                "seeking_talent": True if venue.seeking_talent in (True, 't', 'True') else False,
                "seeking_description": venue.seeking_description,
                "image_link": venue.image_link if venue.image_link else "",
                "past_shows_count": venue.num_past_shows,
                "upcoming_shows_count": venue.num_upcoming_shows,
            }

            for show in venue.past_shows:
                artist = Artist.query.get(show.artist_id)
                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": str(show.start_time)
                })

            for show in venue.upcoming_shows:
                artist = Artist.query.get(show.artist_id)
                upcoming_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": str(show.start_time)
                })

        data["past_shows"] = past_shows
        data["upcoming_shows"] = upcoming_shows
        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @ classmethod
    def update_venue(cls, form_data, venue_id):
        updated_venue = cls.query.get(venue_id)
        genre_formated = ', '.join(str(e)for e in form_data.genres.data)
        try:
            updated_venue.name = form_data.name.data
            updated_venue.genres = ','.join(
                str(e)for e in form_data.genres.data)
            updated_venue.address = form_data.address.data
            updated_venue.city = form_data.city.data
            updated_venue.state = form_data.state.data
            updated_venue.phone = form_data.phone.data
            updated_venue.website = form_data.website_link.data
            updated_venue.facebook_link = form_data.facebook_link.data
            updated_venue.seeking_talent = True if form_data.seeking_talent.data in (
                True, 't', 'True') else False
            updated_venue.seeking_description = form_data.seeking_description.data
            updated_venue.image_link = form_data.image_link.data if form_data.image_link.data else ""

            db.session.commit()
            error = False

        except Exception as e:
            db.session.rollback()
            return False

        return True

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


#############################################################################################################
##                                          Artist Model                                                   ##
#############################################################################################################

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
    shows = db.relationship('Show', backref='Artist', lazy=True)

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

    @property
    def upcoming_shows(self):
        upcoming_shows = [
            show for show in self.shows if show.start_time > datetime.now()]
        return upcoming_shows

    @property
    def num_upcoming_shows(self):
        return len(self.upcoming_shows)

    @property
    def past_shows(self):
        past_shows = [
            show for show in self.shows if show.start_time < datetime.now()]

        return past_shows

    @property
    def num_past_shows(self):
        return len(self.past_shows)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def artist_exists(cls, name):
        artist_exisits = cls.query.filter_by(name=name).first()
        if artist_exisits:
            return True
        else:
            return False

    @classmethod
    def list_artists(cls):
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
        data = Artist.query.with_entities(Artist.id, Artist.name).all()
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
        artist = cls.query.get(artist_id)
        past_shows = []
        upcoming_shows = []
        for show in artist.past_shows:
            venue = Venue.query.get(show.venue_id)
            past_shows.append({
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time
            })
        for show in artist.upcoming_shows:
            venue = Venue.query.get(show.venue_id)
            upcoming_shows.append({
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time
            })
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
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": artist.num_past_shows,
            "upcoming_shows_count": artist.num_upcoming_shows

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


#############################################################################################################
##                                          Show Model                                                     ##
#############################################################################################################

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def __repr__(self):
        return '<Show {}{}>'.format(self.artist_id, self.venue_id)

    def __init__(self, start_time, artist_id, venue_id):
        self.start_time = start_time
        self.artist_id = artist_id
        self.venue_id = venue_id

    @classmethod
    def list_shows(cls):
        data = []
        shows = db.session.query(
            cls.artist_id, cls.venue_id, cls.start_time).all()

        for show in shows:
            artist = db.session.query(Artist.name, Artist.image_link).filter(
                Artist.id == show[0]).one()
            venue = db.session.query(Venue.name).filter(
                Venue.id == show[1]).one()
            data.append({
                "venue_id": show[1],
                "venue_name": venue[0],
                "artist_id": show[0],
                "artist_name": artist[0],
                "artist_image_link": artist[1],
                "start_time": str(show[2])
            })

        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
