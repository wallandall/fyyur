from sqlalchemy.orm import query
from db import db
import datetime


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

    @ property
    def num_upcoming_shows(self):
        return len(self.upcoming_shows)

    @ property
    def past_shows(self):
        past_shows = [
            show for show in self.shows if show.start_time < datetime.now()]
        return past_shows

    @ property
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
        city = cls.query.with_entities(
            cls.city, cls.state).distinct().all()
        for c in city:
            city = c.city
            state = c.state
            venues = cls.query.filter_by(city=city, state=state).all()
            # shows = venues[0].upcoming_shows
            data.append({
                "city": city,
                "state": state,
                "venues": venues
            })
        return data

    @ classmethod
    def show_venue(cls, venue_id):
        venue = cls.query.get(venue_id)

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
            "past_shows": [{
                "artist_id": 5,
                "artist_name": "Matt Quevedo",
                "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }],  # List
            "upcomming_shows": [{
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }],  # List
            "past_shows_count": len(Show.query.filter(
                Show.start_time < datetime.datetime.now(),
                Show.venue_id == self.id).all()),  # Int
            "upcomming_shows_count": 6  # Int

        }

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
