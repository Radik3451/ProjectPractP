from flask import Blueprint, jsonify, request, abort
from flask_restful import Resource, Api
from users import db, User
from users_parser import user_parser

users_resource_bp = Blueprint('users_resource', __name__)
api = Api(users_resource_bp)

class UsersListResource(Resource):
    def get(self):
        users = User.query.all()
        users_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(users_list)

    def post(self):
        args = user_parser.parse_args()
        new_user = User(name=args['name'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'})

class UsersResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            abort(404)
        user_info = {'id': user.id, 'name': user.name, 'email': user.email}
        return jsonify(user_info)

    def put(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            abort(404)

        args = user_parser.parse_args()
        user.name = args['name']
        user.email = args['email']
        db.session.commit()

        return jsonify({'message': 'User edited successfully'})

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            abort(404)

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'})

api.add_resource(UsersListResource, '/users')
api.add_resource(UsersResource, '/users/<int:user_id>')
