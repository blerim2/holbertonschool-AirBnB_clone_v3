#!/usr/bin/python3
""" Module to create API endpoints"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_places(city_id=None):
    """func to return places"""
    city = storage.get(City, city_id)

    if city is None:
        return abort(404)
    if request.method == 'GET':
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        if not data:
            return abort(400, description="Not a JSON")
        if "user_id" not in data:
            return abort(400, description="Missing user_id")
        user_id = data["user_id"]
        if storage.get(User, user_id) is None:
            return abort(404)
        if "name" not in data:
            return abort(400, description="Missing name")
        new_place = Place(**data)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['DELETE', 'GET', 'PUT'], strict_slashes=False)
def delete_place(place_id=None):
    """func to delete objects"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == 'GET':
        return jsonify(place.to_dict()), 200
    if request.method == 'PUT':
        data = request.get_json(force=True)
        if not data:
            return abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'updated_at', 'created_at',
                         'user_id', 'city_id']:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
