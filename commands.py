from csv_utils import load_from_csv
from database import db
from models import ProductDetails, ProductReviews


def create_db():
    db.create_all()


def drop_db():
    db.drop_all()


def create_model_table():
    ProductDetails.__table__.create(db.engine)


def init_app(app):
    for command in [create_db, drop_db, create_model_table, prepopulate]:
        app.cli.add_command(app.cli.command()(command))


def prepopulate():
    ProductDetails.map_save_bulk(load_from_csv("static/products.csv"))
    ProductReviews.map_save_bulk(load_from_csv("static/reviews.csv"))
