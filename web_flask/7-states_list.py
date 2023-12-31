#!/usr/bin/python3

"""
script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
route /states_list: display list of states
"""


from flask import Flask, render_template
import models
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def getStatesList():
    """ returns list of states """
    if models.hbnb_type_storage == "db":
        states = models.storage.all("State").values()
    else:
        states = models.storage.all(State).values()

    states = sorted(states, key=lambda state: state.name)
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown_db(exception=None):
    models.storage.close()


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0")
