#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment

from flask_migrate import Migrate, show
import logging
from logging import DEBUG, Formatter, FileHandler
from flask_wtf import Form
from forms import *
from config import DevConfig
from db import db
from models.artist import Artist
from models.show import Show
from models.venue import Venue
import traceback

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object(DevConfig)
db.init_app(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = Venue.list_venue()

    return render_template('pages/venues.html', areas=data)

# Search fo a Venue


@app.route('/venues/search', methods=['POST'])
def search_venues():

    search_term = request.form.get('search_term', '')
    response = Venue.find_by_name(search_term)
    return render_template('pages/search_venues.html', results=response, search_term=search_term)

# Display a venue


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = Venue.show_venue(venue_id)

    return render_template('pages/show_venue.html', venue=data)


#  Display the Add Venue Form


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

# Create a venue


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    form_data = VenueForm(request.form)
    if Venue.venue_exists(form_data.name.data):
        flash('Venue ' + form_data.name.data + ' already exists!')
        return render_template('pages/home.html')
    try:
        new_venue = Venue(
            name=form_data.name.data,
            genres=form_data.genres.data,
            address=form_data.address.data,
            city=form_data.city.data,
            state=form_data.state.data,
            phone=form_data.state.data,
            website=form_data.website_link.data,
            facebook_link=form_data.facebook_link.data,
            seeking_talent=form_data.seeking_talent.data,
            seeking_description=form_data.seeking_description.data,
            image_link=form_data.image_link.data

        )
        new_venue.save_to_db()
        flash('Venue ' + form_data.name.data + ' was successfully listed!')
    except Exception as ex:
        flash('An error occurred. Venue ' +
              form_data.name.data + ' could not be listed.')
        traceback.print_exc()
    return render_template('pages/home.html')

# Delete a Venue


@ app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

    v = Venue.query.get(venue_id)

    try:
        v.delete_from_db()
        flash('Venue  was successfully deleted!')

    except Exception as ex:
        ('Could not delete the venue!')
        traceback.print_exc()

    return None


#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():

    data = Artist.list_artis()
    return render_template('pages/artists.html', artists=data)

# Search for an artist


@ app.route('/artists/search', methods=['POST'])
def search_artists():

    search_term = request.form.get('search_term', '')
    response = Artist.find_artist(search_term)
    return render_template('pages/search_artists.html', results=response, search_term=search_term)

# Display an artist


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = Artist.show_artist(artist_id)

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------

# Display the update form


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.show_artist(artist_id)
    form = ArtistForm(data=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

# Update Artist


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # artist = Artist.show_artist(artist_id)

    form_data = ArtistForm(request.form)

    if Artist.update_artist(form_data, artist_id):
        flash(form_data.name.data + ' was successfully updated!')
    else:
        flash(form_data.name.data + ' could not be updated!')

    return redirect(url_for('show_artist', artist_id=artist_id))

#   Display Venue Update Form


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.show_venue(venue_id)
    form = VenueForm(data=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)

# Update a Venue


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form_data = VenueForm(request.form)

    if Venue.update_venue(form_data, venue_id):
        flash(form_data.name.data + ' was successfully updated!')
    else:
        flash(form_data.name.data + ' could not be updated!')

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
