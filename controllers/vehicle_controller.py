# controllers/vehicle_controller.py

from flask import Blueprint, request
import os
import sys
import json

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

from functions.similar_model import get_similar_vehicle, get_similar_vehicle_bybedrock

vehicle_blueprint = Blueprint('vehicle', __name__)

@vehicle_blueprint.route('/')
def vehicle_home():
    return "Vehicle Home"

@vehicle_blueprint.route('/similar_vehicle')
async def similar_vehicle():
    user_input = request.args.get("userInput")
    make = request.args.get("make")
    brand = request.args.get("brand")
    res = await get_similar_vehicle(user_input, make , brand)
    return json.dumps(res)

@vehicle_blueprint.route('/similar_vehicle_bybedrock')
async def similar_vehicle_bybedrock():
    user_input = request.args.get("userInput")
    make = request.args.get("make")
    brand = request.args.get("brand")
    res = await get_similar_vehicle_bybedrock(user_input, make , brand)
    return json.dumps(res)

@vehicle_blueprint.route('/vehicle_details')
def vehicle_details():
    return "Vehicle Details"

@vehicle_blueprint.route('/compare_vehicle')
def compare_vehicle():
    return "Compare Vehicles"
