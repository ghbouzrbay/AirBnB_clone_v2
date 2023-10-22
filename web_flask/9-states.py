#!/usr/bin/python3
""" Starts a Flask web app """
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)

@app.route('/states', strict_slashes=False)
def states():
    """display the states and cities listed in alphabetical order"""
    states = storage.all("State")
    return render_template("9-states.html", states=states)

@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Displays an HTML page with info about <id>, if it exists"""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", states=states)
    return render_template("9-states.html")

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
