#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models import storage

app = Flask(__name)

@app.teardown_appcontext
def teardown_session(exception):
    storage.close()

@app.route('/states_list', strict_slashes=False)
def states_list():
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)

    return render_template('states_list.html', states=sorted_states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
