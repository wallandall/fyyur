from db import db


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
