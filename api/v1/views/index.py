#!/usr/bin/python3
"""
Connect to api
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """returns status ok"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats')
def numtypes():
    dicty = {}
    amenC = storage.count("Amenity")
    dicty["amenities"] = amenC
    cityC = storage.count("City")
    dicty["cities"] = cityC
    placeC = storage.count("Place")
    dicty["places"] = placeC
    reviewC = storage.count("Review")
    dicty["reviews"] = reviewC
    stateC = storage.count("State")
    dicty["states"] = stateC
    userC = storage.count("User")
    dicty["users"] = userC

    return jsonify(dicty)
