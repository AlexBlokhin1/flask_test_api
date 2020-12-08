from database import db
from sqlalchemy.orm import relationship


class ProductDetails(db.Model):
    __tablename__ = 'product_details'

    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String())
    title = db.Column(db.String())

    def __init__(self, title, asin):
        self.asin = asin
        self.title = title

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'asin': self.asin,
            'title': self.title,
        }


class ProductReviews(db.Model):
    __tablename__ = 'product_reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_details.id'))
    asin = db.Column(db.String())
    title = db.Column(db.String())
    review = db.Column(db.String())

    def __init__(self, product_id, title, asin, review):
        self.product_id = product_id
        self.asin = asin
        self.title = title
        self.review = review

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'asin': self.asin,
            'title': self.title,
            'review': self.review
        }

    product_details = relationship("ProductDetails")
