#!/usr/bin/python3
"""App to perform actions"""


from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['0.0.0.0'])
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """Close storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
