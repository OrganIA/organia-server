import flask

from . import db
from .application import App


def create_app():
    app = App()

    @app.get('/')
    def root():
        # TODO fix route name
        return flask.redirect(flask.url_for('app_api.root'))

    from .api import bp

    app.register_blueprint(bp)

    app.teardown_appcontext(db.teardown)

    from .errors import register_error_handler

    register_error_handler(app)

    return app
