from db import db


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    artist = db.relationship(
        'Artist', backref=db.backref('shows', cascade='all, delete'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    venue = db.relationship(
        'Venue', backref=db.backref('shows', cascade='all, delete'))
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Show {}{}>'.format(self.artist_id, self.venue_id)

    def __init__(self, artist_id, artist, city, state, phone, website, facebook_link, seeking_venue, seeking_description, image_link):
        self.artist_id = artist_id
        self.artist = artist
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.image_link = image_link
