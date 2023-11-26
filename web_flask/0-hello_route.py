#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/airbnb-onepage/')
def index():
    """display "Hello HBNB!"

    Returns:
        str: text on the index page
    """
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=None)
