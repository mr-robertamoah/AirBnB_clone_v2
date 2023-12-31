#!/usr/bin/python3

"""
script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
route /cities_by_states: display list of states
"""


from flask import Flask, render_template
import models
from models.state import State


app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def getStatesListWithCities():
    """ returns list of states """
    if models.hbnb_type_storage == "db":
        states = models.storage.all("State").values()
    else:
        states = models.storage.all(State).values()

    states = sorted(states, key=lambda state: state.name)
    for state in states:
        state.cities.sort(key=lambda city: city.name)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown_db(exception=None):
    models.storage.close()


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0")
