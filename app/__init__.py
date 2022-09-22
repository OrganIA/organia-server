import flask

from . import db, errors, log
from .application import App, TestApp


def create_app(test=False):
    if not test:
        app = App()
    else:
        app = TestApp()

    @app.get('/')
    def root():
        # TODO fix route name
        return flask.redirect(flask.url_for('app_api.root'))

    from .api import bp

    app.register_blueprint(bp)

    app.register_error_handler(errors.HTTPException, errors.error_handler_http)

    app.before_request(log.log_request)

    app.before_request(db.before_request)
    app.after_request(db.after_request)

    return app


from app.utils.bp import Blueprint as Blueprint
from app.utils.static import Static as Static
