from flask import abort, jsonify
from flask_restful import Resource

from data import db_session
from data.users import User
from user_req_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'about', 'email', 'created_date'))})

    def delete(self, products_id):
        abort_if_user_not_found(products_id)
        session = db_session.create_session()
        user = session.query(User).get(products_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        products = session.query(User).all()
        return jsonify({'user': [item.to_dict(only=('name', 'about', 'email', 'created_date')) for item in products]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            about=args['about'],
            email=args['email'],
            created_date=args['created_date'])
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
