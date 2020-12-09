from csv_utils import get_dict_data, get_dict_data_2
from database import db
from models import ProductDetails, ProductReviews


def create_db():
    db.create_all()


def drop_db():
    db.drop_all()


def create_model_table():
    ProductDetails.__table__.create(db.engine)


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, create_model_table, prepopulate]:
        app.cli.add_command(app.cli.command()(command))


def prepopulate():
    data = get_dict_data("static/products.csv")
    for i in data.items():
        details = ProductDetails(asin=i[0], title=i[1])
        db.session.add(details)
    db.session.commit()

    data = get_dict_data_2("static/reviews.csv")
    for i in data.items():
        product_id = db.session.query(ProductDetails).filter_by(asin=i[1][0]).first().id
        details = ProductReviews(asin=i[1][0], title=i[0], review=i[1][1], product_id=product_id)
        db.session.add(details)
    db.session.commit()