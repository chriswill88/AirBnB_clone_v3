#!/usr/bin/python3
"""
creates a Flask web application
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(err):
    """closes storage session"""
    storage.close()


@app.errorhandler(404)
def error_status_code(error):
    """handles 404 errors: Returns json error not found"""
    return ({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(
        host=os.getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=os.getenv('HBNB_API_PORT', default=5000),
        threaded=True
    )
