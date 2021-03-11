from flask_sqlalchemy import SQLAlchemy
from cachelib import SimpleCache
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP
from flask import Flask, jsonify, request, make_response, abort
import os
import argparse
import datetime

app = Flask(__name__)
print(os.getenv('SQLALCHEMY_DATABASE_URI'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
cache = SimpleCache()


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    asin = db.Column('asin', db.String())
    title = db.Column('title', TEXT)
    created_at = db.Column(
        'created_at', TIMESTAMP, nullable=False, default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        'updated_at', TIMESTAMP, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    asin_id = db.Column('asin_id', db.Integer, db.ForeignKey('products.id'), index=True)
    title = db.Column('title', TEXT)
    review = db.Column('review', TEXT)
    created_at = db.Column(
        'created_at', TIMESTAMP, nullable=False, default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        'updated_at', TIMESTAMP, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def __init__(self, asin_id, title, review):
        self.asin_id = asin_id
        self.title = title
        self.review = review


@app.route('/product/<int:id>', methods=['GET'], defaults={"start": 1, "limit": 20})
@app.route('/product/<int:id>/<int:start>', methods=['GET'], defaults={"limit": 20})
@app.route('/product/<int:id>/<int:start>/<int:limit>', methods=['GET'])
def product(id, start, limit):
    try:
        hash = f'{int(id)}#{int(start)}#{int(limit)}'
        data = cache.get(hash)
        if not data:
            raw_rows = db.session.query(Products, Reviews)\
                .join(Reviews)\
                .filter(int(id) == Products.id)\
                .paginate(int(start), int(limit), False)\
                .items
            rows = [
                {
                    'product_asin': row.Products.asin,
                    'product_title': row.Products.title,
                    'review_title':  row.Reviews.title,
                    'review_review': row.Reviews.review
                } for row in raw_rows
            ]
            cache.set(hash, rows)
        else:
            rows = data
        return jsonify(rows)
    except Exception as exc:
        abort(500)


@app.route('/reviews/<int:id>', methods=['PUT'])
def reviews(id):
    try:
        product_id = int(id)
        req = request.get_json()
        title = req.get('title', None)
        review = req.get('review', None)
        if all((product_id, title, review)):
            product_db_id = db.session.query(Products).filter(product_id == Products.id).first()
            if product_db_id:
                review_row = Reviews(asin_id=product_db_id.id, title=title, review=review)
                db.session.add(review_row)
                db.session.commit()
                return make_response(jsonify({'result': True}), 200)
            else:
                return make_response(
                    jsonify({'result': False, 'reason': f'Product with ID {product_id} not found'}), 404
                )
        else:
            return make_response(
                jsonify({'result': False, 'reason': 'Not all required fields are filled in the request'}), 404
            )
    except Exception as exc:
        abort(500)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test API')
    parser.add_argument('--host', help='Host', default='0.0.0.0')
    parser.add_argument('--port', help='Port', default=8888)
    app.run(host=parser.parse_args().host, port=int(parser.parse_args().port))
