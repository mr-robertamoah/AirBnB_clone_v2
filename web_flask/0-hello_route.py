#!/usr/bin/python3

"""
script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
route /: display 'Hello HBNB!'
"""


from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """ returns a string """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0")
