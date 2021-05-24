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
    shows = db.relationship('Show', backref='Venue',
                            lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, name, generes, address, city, state, phone, website, facebook_link, seeking_talent, seeking_description, image_link, shows):
        self.name = name
        self.generes = generes
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description
        self.image_link = image_link
        self.show = shows

    @classmethod
    def find_by_state(cls, state):
        return cls.query.filter_by(state=state)

    @classmethod
    def find_all(cls):
        return cls.query.all()

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
