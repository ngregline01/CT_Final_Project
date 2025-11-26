from .models import db
from flask import Flask
from Mechanic_App.extensions import ma, limiter, cache
from Mechanic_App.blueprints.customers import customers_bp
from Mechanic_App.blueprints.mechanics import mechanics_bp
from Mechanic_App.blueprints.service_tickets import tickets_bp
from Mechanic_App.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API's Name"
    }
)

#Create the app
def create_app(config_name):
    mechanics_shop = Flask(__name__)
    mechanics_shop.config.from_object(f'config.{config_name}')

    #Add the app to the db connections
    db.init_app(mechanics_shop)
    ma.init_app(mechanics_shop)
    limiter.init_app(mechanics_shop)
    cache.init_app(mechanics_shop)

#Register the blueprint
    mechanics_shop.register_blueprint(customers_bp, url_prefix="/customers")
    mechanics_shop.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    mechanics_shop.register_blueprint(tickets_bp, url_prefix="/service_tickets")
    mechanics_shop.register_blueprint(inventory_bp, url_prefix="/inventory" )
    mechanics_shop.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint
    return mechanics_shop


