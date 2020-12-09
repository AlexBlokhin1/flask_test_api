from database import db
import commands


def init_ext(app):
    db.init_app(app)
    commands.init_app(app)
