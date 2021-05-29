from db import db


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

    @classmethod
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

    @classmethod
    def venue_exists(cls, name):
        venue_exisits = cls.query.filter_by(name=name).first()
        if venue_exisits:
            return True
        else:
            return False

    @classmethod
    def list_venue(cls):
        data = []
        city = Venue.query.with_entities(
            Venue.city, Venue.state).distinct().all()
        for c in city:
            city = c.city
            state = c.state
            venues = Venue.query.filter_by(city=city, state=state).all()
            #shows = venues[0].upcoming_shows
            data.append({
                "city": city,
                "state": state,
                "venues": venues
            })
        return data

    @classmethod
    def show_venue(cls, venue_id):
        venue = Venue.query.get(venue_id)

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
            "past_shows": [],  # add a class function
            "upcomming_shows": [],  # zadd a class function
            "past_shows_count": 5,  # zadd a class function
            "upcomming_shows_count": 6  # zadd a class function

        }

        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
