#!/usr/bin/python3
""" Module to create API endpoints"""
from models import storage
from models.user import User
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def return_users(user_id=None):
    """Func to retrieve users"""

    if request.method == 'GET':
        if user_id is None:
            users = []
            for user in storage.all(User).values():
                users.append(user.to_dict())
            return jsonify(users)
        user = storage.get(User, user_id)
        if user is None:
            return abort(404)
        return jsonify(user.to_dict())
    if request.method == 'PUT':
        user = storage.get(User, user_id)
        if user is None:
            return abort(404)
        data = request.get_json(force=True)
        if not data:
            return abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'updated_at', 'created_at', 'email']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        if user_id is None:
            return abort(404)
        user = storage.get(User, user_id)
        if user is None:
            return abort(404)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        if not data:
            return abort(400, description="Not a JSON")
        if "email" not in data:
            return abort(400, description="Missing email")
        if "password" not in data:
            return abort(400, description="Missing password")
        new_user = User(**data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
