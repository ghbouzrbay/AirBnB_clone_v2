#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception=None):
    """removes the current SQLAlchemy Session
    """
    if storage is not None:
        storage.close()


@app.route('/hbnb_filters')
def hbnb_filters(id=None):
    """displays a HTML page: inside the tag BODY"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


if __name__ == '__main__':
    app.run(debug=True)
