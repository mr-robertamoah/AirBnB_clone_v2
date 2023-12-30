#!/usr/bin/python3

"""
script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
route /: display 'Hello HBNB!'
route /hbnb: display 'HBNB'
route /c/<text>: display C followed by the value of the text
    variable (replace underscore _ symbols with a space)
route /python/<text>: display Python, followed by the value of the
    text variable (replace underscore _ symbols with a space)
"""


from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """ returns a string """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ returns a string """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ returns a string """
    text = text.replace("_", " ")
    return f"C {text}"


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """ returns a string """
    text = text.replace("_", " ")
    return f"Python {text}"


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0")
