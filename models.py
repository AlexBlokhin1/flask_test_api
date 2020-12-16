from sqlalchemy.orm import relationship

from database import db


class ProductDetails(db.Model):
    __tablename__ = 'product_details'

    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String())
    title = db.Column(db.String())

    @classmethod
    def map_save_bulk(cls, data):
        for el in data:
            details = cls(**el)
            db.session.add(details)
        db.session.commit()

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
    product = relationship("ProductDetails")
    title = db.Column(db.String())
    review = db.Column(db.String())

    @classmethod
    def map_save_bulk(cls, data):
        for el in data:
            product_id = db.session.query(ProductDetails).filter_by(asin=el['asin']).first().id
            details = cls(product_id=product_id, **el)
            db.session.add(details)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'asin': self.asin,
            'title': self.title,
            'review': self.review,
            'product': self.product.serialize(),
        }
