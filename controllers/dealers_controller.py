# controllers/dealers_controller.py

from flask import Blueprint

dealers_blueprint = Blueprint('dealers', __name__)

@dealers_blueprint.route('/')
def dealers_home():
    return "Dealers Home"

@dealers_blueprint.route('/list')
def list_dealers():
    return "List of Dealers"

@dealers_blueprint.route('/register')
def register_dealer():
    return "Register a Dealer"
