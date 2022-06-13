import flask

from app.utils.flask import Flask


app = Flask(__name__)


@app.get('/')
def root():
    return flask.redirect(flask.url_for('api.root'))


from app.utils.bp import Blueprint
from app.utils.flask import Flask
from app.utils.static import Static


from .api import bp
app.register_blueprint(bp)
