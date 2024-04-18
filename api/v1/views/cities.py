#!/usr/bin/python3
""" Module to create API endpoints"""
from models import storage
from models.state import State
from models.city import City
from flask import jsonify,request,abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_cities(state_id=None):
    """ view func to retrieve data"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if request.method == 'GET':
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        if not data:
            return abort(400, description="Not a JSON")
        if "name" not in data:
            return abort(400, description="Missing name")
        new_city = City(name=data["name"], state_id=state_id)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['DELETE', 'GET', 'PUT'], strict_slashes=False)
def delete_city(city_id=None):
    """ view func to retrieve data"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'GET':
        return jsonify(city.to_dict()), 200
    if request.method == 'PUT':
        city_dict = city.to_dict()
        data = request.get_json(force=True)
        if not data:
            return abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'updated_at', 'created_at', 'state_id']:
                city_dict[key] = data[key]
        storage.save()
        return jsonify(city_dict), 200
