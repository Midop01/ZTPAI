from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/')
def api_index():
    return jsonify({"message": "API is working"})

# Import other routes
from .auth import *
from .comments import *
from .images import *
from .posts import *
from .likes import *
