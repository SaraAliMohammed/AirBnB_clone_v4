#!/usr/bin/python3
"""City module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from flasgger.utils import swag_from


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities_in_state(state_id):
    """ get all cities in state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [c.to_dict() for c in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """ get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def del_city(city_id):
    """ delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def create_city(state_id):
    """ create new instance """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        return make_response("Not a JSON", 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    new_city = City(**js)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """ update method """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
