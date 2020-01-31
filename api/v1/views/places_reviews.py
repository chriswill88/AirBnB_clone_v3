#!/usr/bin/python3
"""
Create a new view for review
"""
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.review import Review
from models.place import Place


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """retrieves all review objects based on place_id"""
    review_list = []
    # check place obj from place_id
    if storage.get('Place', place_id) is None:
        abort(404)
    # pulling out all reviews for work
    reviews = storage.all('Review').values()
    # for review in reviews find the obj with the right
    # id for the list.
    for review in reviews:
        if review.place_id == place_id:
            review_list.append(review.to_dict())
    return (jsonify(review_list))


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """retrieves a single review object"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    else:
        return (jsonify(review_obj.to_dict()))


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a Review by ID"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """create a review"""
    # get place obj to change
    if storage.get("Place", place_id) is None:
        abort(404)
    # check the request.json
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    if "user_id" not in request.get_json():
        return (jsonify({"error": "Missing user_id"})), 400
    json_dict = request.get_json()
    # check user_id
    user_id = json_dict["user_id"]
    if storage.get("User", user_id):
        abort(404)
    # check text in json_dict
    if "text" not in json_dict:
        return (jsonify({"error": "Missing text"})), 400
    # adding place_id | possibly foriegn key
    json_dict["place_id"] = place_id
    new_review = Review(**json_dict)
    new_review.save()
    return (jsonify(new_review.to_dict())), 201


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """updates a review object"""
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review = storage.get('Place', review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(review, k, v)
    storage.save()
    return (jsonify(review.to_dict())), 200
