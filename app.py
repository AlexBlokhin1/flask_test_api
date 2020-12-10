import logging
import os

from flask import Flask, request, jsonify, render_template

from database import db
from extentions import init_ext
from models import ProductDetails, ProductReviews

logger = logging.getLogger(__name__)


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


init_ext(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/<int:id>", methods=['GET'])
def get_product_details(id):
    product_details = ProductDetails.query.get(id)
    product_reviews = ProductReviews.query.get(id).review
    result = {"asin": product_details.asin, "title": product_details.title, "reviews": product_reviews}
    logger.debug('information by id {}: {}'.format(id, result))
    return jsonify(result)


@app.route('/review')
def review():
    return render_template('review_form.html')


@app.route("/review", methods=['POST'])
def review_post():
    product_id = request.form['id']
    title = request.form['title']
    review = request.form['review']

    product_details = ProductDetails.query.get(product_id)
    asin = product_details.asin

    new_review = ProductReviews(product_id=product_id, asin=asin, title=title, review=review)
    db.session.add(new_review)
    db.session.commit()

    logger.debug('review has been added: {}'.format(new_review))
    return jsonify(new_review.serialize())


if __name__ == '__main__':
    app.run()
