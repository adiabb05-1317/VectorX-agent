from flask import Blueprint, request, jsonify, current_app
from src.database.db import DatabasePool
from src.workflows import immigration_workflow


main_bp = Blueprint('main_bp',__name__)


@main_bp.route('/')
def index():
    return jsonify({'statys': 'healthy'})
