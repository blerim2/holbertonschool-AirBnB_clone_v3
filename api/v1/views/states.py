#!/usr/bin/python3
""" Module to create an API endpoint"""
from models import storage
from models.state import State
from flask import jsonify,request,abort
from api.v1.views import app_views
import json


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def return_states(state_id=None):
    """view to return form API"""

    if request.method == 'GET':
        if state_id is None:
            states = []
            for state in storage.all(State).values():
                states.append(state.to_dict())
            return jsonify(states)
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        return jsonify(state.to_dict())
    if request.method == 'PUT':
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        data = request.get_json(force=True)
        if not data:
            return abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'updated_at', 'created_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        if state_id is None:
            return abort(404)
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        if not data:
            return abort(400, description="Not a JSON")
        if "name" not in data:
            return abort(400, description="Missing name")
        new_state = State(name=data["name"])
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
