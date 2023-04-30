from flask import Blueprint, jsonify, request

from data import db_session
from data.products import Products

blueprint = Blueprint(
    'products_api',
    __name__,
    template_folder='templates')


@blueprint.route('/api/products')
def get_products():
    db_sess = db_session.create_session()
    products =  db_sess.query(Products).all()
    return jsonify({'products': [item.to_dict(only=('title', 'content', 'user.name')) for item in products]})


@blueprint.route('/api/products/<int:products_id>', methods=['GET'])
def get_one_products(products_id):
    db_sess = db_session.create_session()
    products = db_sess.query(Products).get(products_id)
    if not products:
        return jsonify({'error': 'Not found'})
    return jsonify({'products': products.to_dict(only=('title', 'content', 'user_id', 'is_private'))})


@blueprint.route('/api/products', methods=['POST'])
def create_products():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    products = Products(title=request.json['title'],
                        content=request.json['content'],
                        user_id=request.json['user_id'],
                        is_private=request.json['is_private'])
    db_sess.add(products)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/products/<int:products_id>', methods=['DELETE'])
def delete_products(products_id):
    db_sess = db_session.create_session()
    products = db_sess.query(Products).get(products_id)
    if not products:
        return jsonify({'error': 'Not found'})
    db_sess.delete(products)
    db_sess.commit()
    return jsonify({'success': 'OK'})
