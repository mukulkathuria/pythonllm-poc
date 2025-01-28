# controllers/leads_controller.py

from flask import Blueprint

leads_blueprint = Blueprint('leads', __name__)

@leads_blueprint.route('/')
def leads_home():
    return "Leads Home"

@leads_blueprint.route('/create')
def create_lead():
    return "Create a Lead"

@leads_blueprint.route('/update')
def update_lead():
    return "Update a Lead"

@leads_blueprint.route('/delete')
def delete_lead():
    return "Delete a Lead"
