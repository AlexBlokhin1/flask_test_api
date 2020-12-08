import os

from flask import Flask, request, jsonify, render_template

import commands
import database
from csv_utils import get_dict_data, get_dict_data_2
from models import ProductDetails, ProductReviews

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.init_app(app)
commands.init_app(app)


@app.before_first_request
def create_tables():
    database.db.create_all()


@app.route("/load")
def load():
    data = get_dict_data("static/products.csv")
    for i in data.items():
        details = ProductDetails(asin=i[0], title=i[1])
        database.db.session.add(details)
    database.db.session.commit()
    data = get_dict_data_2("static/reviews.csv")

    for i in data.items():
        product_id = database.db.session.query(ProductDetails).filter_by(asin=i[1][0]).first().id
        details = ProductReviews(asin=i[1][0], title=i[0], review=i[1][1], product_id=product_id)
        database.db.session.add(details)
    database.db.session.commit()
    return "data has been loaded"


@app.route("/<int:id>", methods=['GET'])
def get_product_details(id):
    product_details = ProductDetails.query.get(id)
    product_reviews = ProductReviews.query.filter_by(product_id=id).all()
    list_reviews = [x.review for x in product_reviews]
    return jsonify({"asin": product_details.asin, "title": product_details.title, "reviews": list_reviews})


@app.route('/review')
def review():
    return render_template('review_form.html')


@app.route("/review", methods=['PUT', 'POST', 'GET'])
def review_post():
    product_id = request.form['id']
    product_details = ProductDetails.query.get(product_id)
    asin = product_details.asin
    title = request.form['title']
    review = request.form['review']

    new_review = ProductReviews(product_id=product_id, asin=asin, title=title, review=review)
    database.db.session.add(new_review)
    database.db.session.commit()
    return "review has been added"


if __name__ == '__main__':
    app.run()
