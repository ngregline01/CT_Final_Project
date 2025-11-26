from Mechanic_App.models import Mechanics, db 
from Mechanic_App.blueprints.mechanics.schema import mechanics_schema, mechanicschema, login_schema
from Mechanic_App.extensions import limiter, cache
from . import mechanics_bp
from sqlalchemy import select
from marshmallow import ValidationError
from flask import request, jsonify
from Mechanic_App.utils.util import token_required, encode_token

@mechanics_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #make a query to see if the customer trying to login is in your databas
    query = select(Mechanics).where(Mechanics.email==email)
    mechanic = db.session.execute(query).scalars().first()

    #Check if said customer exist and if their password matches the one being entered by the user
    if mechanic and mechanic.password == password:
        token = encode_token(mechanic.id)
        #give the user a response
        response = {
            "response":"Success",
            "Message": "Successfully Logged In",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"Message": "Invalid email or password"}), 400

#Create a mechanic
@mechanics_bp.route("/", methods=['POST'])
#@limiter.limit("5 per month") #You can't hire more than 5 mechanics a month
def create_mechanic():
    try:
        mechanic_data = mechanicschema.load(request.json)
    except ValidationError as e:
        return (e.messages), 400
    
    query = select(Mechanics).where(Mechanics.email==mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().all()

    if existing_mechanic:
        return ({"Error": "Mechanic exists"}), 400
    
    new_mechanic=Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanicschema.jsonify(new_mechanic), 201
    
#Retrieve all mechanics
@mechanics_bp.route("/", methods=['GET'])
#@cache.cached(timeout=30)
def get_mechanics():
    query=select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)

#Update a mechanic
@mechanics_bp.route("/", methods=['PUT'])
@token_required
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"Error": "Mechanic not found"}), 404
    try:
        mechanic_data = mechanicschema.load(request.json)
    except ValidationError as e:
        return (e.messages), 400
    
    for key, value in mechanic_data.items():
        if value not in ("", None):
            setattr(mechanic, key, value)

    db.session.commit()
    return mechanicschema.jsonify(mechanic)

#Delete a mechanic
@mechanics_bp.route("/", methods=['DELETE'])
@token_required
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"Error": "Sorry, mechanic does not exist"})
    
    db.session.delete(mechanic)
    db.session.commit()
    return mechanicschema.jsonify({"Message": f'Mechanice id: {mechanic_id} deleted successfully'}), 200

#Searching for Mechanics with the most tickets
@mechanics_bp.route("/popular", methods=['GET'])
def get_popular_mechanic():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    mechanics.sort(key=lambda m: len(m.tickets), reverse=True) #sort the keys in descending order using the relationship values to get popular tickets

    return mechanics_schema.jsonify(mechanics)


