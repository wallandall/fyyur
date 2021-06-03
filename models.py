

from flask.globals import session
from sqlalchemy.orm import query
from sqlalchemy import func, distinct

from datetime import datetime
from db import db


#############################################################################################################
##                                          Venue Model                                                   ##
#############################################################################################################


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue', lazy=True)

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
        city_state = cls.query.with_entities(func.count(
            cls.id), cls.city, cls.state).group_by(cls.city, cls.state).all()

        for area in city_state:
            area_venues = cls.query.filter_by(
                state=area.state).filter_by(city=area.city).all()
            venue_data = []
            for venue in area_venues:
                venue_data.append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id == 1).filter(Show.start_time > datetime.now()).all())
                })
            data.append({
                "city": area.city,
                "state": area.state,
                "venues": venue_data
            })

        return data

    @ classmethod
    def show_venue(cls, venue_id):
        venue = cls.query.get(venue_id)
        if venue:
            upcoming_shows_query = db.session.query(Show).join(Artist).filter(
                Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
            upcoming_shows = []

            past_shows_query = db.session.query(Show).join(Artist).filter(
                Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
            past_shows = []

            for show in past_shows_query:

                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.Artist.name,
                    "artist_image_link": show.Artist.image_link,
                    "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
                })

            for show in upcoming_shows_query:

                upcoming_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.Artist.name,
                    "artist_image_link": show.Artist.image_link,
                    "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
                })
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
                "seeking_talent": venue.seeking_talent,
                "seeking_description": venue.seeking_description,
                "image_link": venue.image_link,
                "past_shows": past_shows,
                "upcoming_shows": upcoming_shows,
                "past_shows_count": len(past_shows),
                "upcoming_shows_count": len(upcoming_shows),
            }
        else:
            data = []

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

    @ classmethod
    def find_all(cls):
        return cls.query.all()

    @ classmethod
    def artist_exists(cls, name):
        artist_exisits = cls.query.filter_by(name=name).first()
        if artist_exisits:
            return True
        else:
            return False

    @ classmethod
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

    @ classmethod
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
        if artist:
            upcoming_shows_query = db.session.query(Show).join(Venue).filter(
                Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()

            upcoming_shows = []

            past_shows_query = db.session.query(Show).join(Venue).filter(
                Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()

            past_shows = []

            for show in past_shows_query:
                past_shows.append({
                    "artist_id": show.artist_id,
                    "venue_name": show,
                    "venue_image_link": show.Venue.image_link,
                    "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
                })

            for show in upcoming_shows_query:
                upcoming_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": show.Venue.name,
                    "artist_image_link": show.Venue.image_link,
                    "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
                })
            data = {
                "id": artist.id,
                "name": artist.name,
                "genres": artist.genres,
                "city": artist.city,
                "state": artist.state,
                "phone": artist.phone,
                "website": artist.website,
                "facebook_link": artist.facebook_link,
                "seeking_venue": artist.seeking_venue,
                "seeking_description": artist.seeking_description,
                "image_link": artist.image_link,
                "past_shows": past_shows,
                "upcoming_shows": upcoming_shows,
                "past_shows_count": len(past_shows),
                "upcoming_shows_count": len(upcoming_shows),
            }
        else:
            data = []

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

    @classmethod
    def list_shows(cls):
        data = []
        shows = db.session.query(Show).join(Artist).join(Venue).all()

        for show in shows:
            data.append({
                "venue_id": show.venue_id,
                "venue_name": show.Venue.name,
                "artist_id": show.artist_id,
                "artist_name": show.Artist.name,
                "artist_image_link": show.Artist.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
