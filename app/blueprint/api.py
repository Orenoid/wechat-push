from flask import Blueprint
# from flask_cors import CORS
from app.utils.http import Api

api_bp = Blueprint("api", __name__)
# CORS(api_bp)
api = Api(api_bp)
