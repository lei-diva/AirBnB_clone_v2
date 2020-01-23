#!/usr/bin/python3

from models import storage
from models.state import State
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/states/", strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def state(id=None):
    s = storage.all(State).values()
    flag = 0
    if id is None:
        flag = 1
    else:
        for st in s:
            if id == st.id:
                flag = 1
    return render_template("9-states.html", states=s, id=id, flag=flag)


@app.teardown_appcontext
def tear(self):
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
