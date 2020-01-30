#!/usr/bin/python3
"""
create a view for place
"""
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"],
                 strict_slashes=False)
def placefromcity(city_id):
    """Retrieve all places from a city"""
    place_list = []
    if storage.get('City', city_id) is None:
        abort(404)
    places = storage.all('Place').values()
    for place in places:
        if place.city_id == city_id:
            place_list.append(place.to_dict())
    return (jsonify(place_list))


@app_views.route("/places/<city_id>",
                 methods=["GET"],
                 strict_slashes=False)
def place_from_id(place_id):
    """Retrive place from id"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def place_delete(place_id):
    """delete a place"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return (jsonify({})), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """create a new amenity"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    if "user_id" not in request.get_json():
        return (jsonify({"error": "Missing user_id"})), 400
    json_dict = request.get_json()
    user_id = json_dict["user_id"]
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    if "name" not in json_dict:
        return (jsonify({"error": "Missing name"})), 400
    json_dict["city_id"] = city_id
    new_place = Place(**json_dict)
    new_place.save()
    return (jsonify(new_place.to_dict())), 201


@app_views.route("/places/<place_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def place_update(place_id):
    """updates a place object"""
    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(place_obj, k, v)
    storage.save()
    return (jsonify(place_obj.to_dict())), 200
