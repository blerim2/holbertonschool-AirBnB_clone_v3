#!/usr/bin/python3
'''
Modul to create API endpoints
'''
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify
from flask import request
from api.v1.views import app_views
from flask import abort


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_places(city_id=None):
    '''
    Simple route
    '''
    city = storage.get(City, city_id)

    if city is None:
        return abort(404)
    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        if not data:
            return abort(400, description="Not a JSON")
        user_id = data.get("user_id", None)
        place_name = data.get("name", None)
        if user_id is None:
            return abort(400, description="Missing user_id")
        if storage.get(User, user_id) is None:
            return abort(404)
        if place_name is None:
            return abort(400, description="Missing name")
        new_place = Place(name=place_name, user_id=user_id, city_id=city_id)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['DELETE', 'GET', 'PUT'], strict_slashes=False)
def delete_place(place_id=None):
    '''
    Simple route
    '''
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
        for k, v in data.items():
            if k not in ['id', 'updated_at', 'created_at',
                         'user_id', 'city_id']:
                setattr(place, k, data[k])
        storage.save()
        return jsonify(place.to_dict()), 200
