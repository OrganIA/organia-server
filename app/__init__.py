import flask
from flask_sock import Sock
from sqlalchemy.event import listens_for

from app import db
from app.application import App
from app.db.models import Role

sock = Sock()


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

    sock.init_app(app)
    return app


@listens_for(Role.__table__, "after_create")
def roles_table_created(*args, **kwargs):
    admin = Role(
        **{
            'can_edit_users': True,
            'can_edit_hospitals': True,
            'can_edit_listings': True,
            'can_edit_staff': True,
            'can_edit_roles': True,
            'can_edit_persons': True,
            'can_invite': True,
            'name': 'admin',
        }
    )
    default = Role(
        **{
            'can_edit_users': False,
            'can_edit_hospitals': False,
            'can_edit_listings': False,
            'can_edit_staff': False,
            'can_edit_roles': False,
            'can_edit_persons': False,
            'can_invite': False,
            'name': 'default',
        }
    )
    db.session.add_all([admin, default])
    db.session.commit()
