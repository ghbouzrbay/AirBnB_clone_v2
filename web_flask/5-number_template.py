#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """display "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb_route():
    """display "HBNB"
    """
    return "HBNB"


@app.route('/c/<text>')
def c_route(text):
    """display "C", followed by the value of <text>
    Replaces any underscores in <text> with slashes.
    """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', defaults={'text', 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    """display "Python", followed by the value of <text>
    Replaces any underscores in <text> with slashes.

    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """display "n is a number" only if n is an integer

    Args:
        n (integer): number to be displayed on page
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_route(n):
    """display a HTML page only if n is an integer

    H1 tag: "Number: n" inside the tag BODY

    Args:
        n (integer): number to be displayed on page
    """
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
