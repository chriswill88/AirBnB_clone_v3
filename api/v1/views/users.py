#!/usr/bin/python3
"""
Create a new view for User
"""
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route("/users",
                 methods=["GET"],
                 strict_slashes=False)
def get_users():
    """get all users"""
    user_list = []
    users = storage.all('User').values()
    for user in users:
        user_list.append(user.to_dict())
    return (jsonify(user_list))


@app_views.route("/users/<user_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_id_user(user_id):
    """get a user from a user_id"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    else:
        return (jsonify(user_obj.to_dict()))


@app_views.route("/users/<user_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """delete user"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    else:
        storage.delete(user_obj)
        storage.save()
        return (jsonify({})), 200


@app_views.route("/users",
                 methods=["POST"],
                 strict_slashes=False)
def create_user():
    """Create new user"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    json_list = request.get_json()
    if "email" not in json_list:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in json_list:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**json_list)
    new_user.save()
    return (new_user.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update user"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    if not request.json():
        return jsonify({"error": "Not a json"}), 400
    for k, v in request.get_json().items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_obj, k, v)
    storage.save()
    return (jsonify(user_id.to_dict())), 200
