#!/usr/bin/python3

"""
script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
route /states: display list of states
route /states/<id>: display state
"""


from flask import Flask, render_template
import models
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def getStatesListOrState(id=None):
    """ returns list of states """
    if models.hbnb_type_storage == "db":
        states = models.storage.all("State").values()
    else:
        states = models.storage.all(State).values()

    states = sorted(states, key=lambda state: state.name)
    state = None
    if id is not None:
        for s in states:
            if s.id == id:
                state = s
        states = None
    if state is not None:
        state.cities.sort(key=lambda city: city.name)

    return render_template("9-states.html", states=states,
                           state=state)


@app.teardown_appcontext
def teardown_db(exception=None):
    models.storage.close()


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0")
