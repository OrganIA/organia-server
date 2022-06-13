import flask

from .application import App


app = App()


@app.get('/')
def root():
    return flask.redirect(flask.url_for('api.root'))


from app.utils.bp import Blueprint
from app.utils.static import Static


from .api import bp
app.register_blueprint(bp)

from . import errors, log
