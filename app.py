# app.py

from flask import Flask
from controllers.leads_controller import leads_blueprint
from controllers.dealers_controller import dealers_blueprint
from controllers.vehicle_controller import vehicle_blueprint

app = Flask(__name__)

# Register blueprints (controllers)
app.register_blueprint(leads_blueprint, url_prefix='/leads')
app.register_blueprint(dealers_blueprint, url_prefix='/dealers')
app.register_blueprint(vehicle_blueprint, url_prefix='/vehicle')

@app.route('/')
def home():
    return "Welcome to my world"

if __name__ == '__main__':
    app.run(debug=True)
