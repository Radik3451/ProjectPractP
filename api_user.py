from flask import Blueprint, jsonify, request, abort
from users import db, User

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

# Получение всех пользователей
@user_bp.route('', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(users_list)

# Получение одного пользователя
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    user_info = {'id': user.id, 'name': user.name, 'email': user.email}
    return jsonify(user_info)

# Добавление пользователя
@user_bp.route('', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})

# Редактирование пользователя
@user_bp.route('/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']
    db.session.commit()

    return jsonify({'message': 'User edited successfully'})

# Удаление пользователя
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})
