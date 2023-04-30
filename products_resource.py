from flask import abort, jsonify
from flask_restful import Resource, reqparse

from data.products import Products
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('price', required=True, type=int)


def abort_if_products_not_found(products_id):
    session = db_session.create_session()
    products = session.query(Products).get(products_id)
    if not products:
        abort(404, message=f"Products {products_id} not found")


class ProductsResource(Resource):
    def get(self, products_id):
        abort_if_products_not_found(products_id)
        session = db_session.create_session()
        products = session.query(Products).get(products_id)
        return jsonify({'products': products.to_dict(
            only=('title', 'content', 'user_id', 'price'))})

    def delete(self, products_id):
        abort_if_products_not_found(products_id)
        session = db_session.create_session()
        products = session.query(Products).get(products_id)
        session.delete(products)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        products = session.query(Products).all()
        return jsonify({'products': [item.to_dict(
            only=('title', 'content', 'user.name', 'price')) for item in products]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        products = Products(title=args['title'],
                            content=args['content'],
                            user_id=args['user_id'],
                            price=args['price'])
        session.add(products)
        session.commit()
        return jsonify({'success': 'OK'})
