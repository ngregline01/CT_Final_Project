from . import inventory_bp # The "." was used because route and init are in the same folder
from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from Mechanic_App.blueprints.inventory.schema import inventorys_schema, inventoryschema
from Mechanic_App.models import Inventory, db


#Create a Part
@inventory_bp.route( "/", methods=['POST'])
def create_part():
    try: #put validation on the customer info that is being fire or sent to the server
        part_data = inventoryschema.load(request.json)#we use the schema so validation can use on the data seamlessly
    except ValidationError as e:
        return jsonify(e.messages), 400 #if the data does not match the expected pattern then it is return as a bad request

    query = select(Inventory).where(Inventory.name==part_data['name']) #this to find a specific customer that aligns with the email because this email is actually unique too
    existing_part = db.session.execute(query).scalars().all() #select all the info that matches the query
    if existing_part:
        return jsonify({"Message": "part already exist"}), 400 #error because the customer exist
    new_part = Inventory(**part_data) #destructure the customer data to create a new_customer
    db.session.add(new_part) #add the new customer to the session
    db.session.commit() #commit it
    return inventoryschema.jsonify(new_part), 201 #return the new_customer, using customer schema

#Retreive all inventory
@inventory_bp.route("/", methods=['GET'] )
def get_parts():
    query = select(Inventory) #This is used to get all of the inventory
    parts = db.session.execute(query).scalars().all() #then you get all the inventory that match the inventory
    return inventorys_schema.jsonify(parts), 200 #this display the inventory


#Retrieve a Single part
@inventory_bp.route("/<int:part_id>", methods=['GET'])
def get_one_part(part_id):
    #using the get method with path parameter
    part_data = db.session.get(Inventory, part_id) #getting the exact part with specific id using path parameter
    if part_data:
        return inventoryschema.jsonify(part_data)
    return jsonify({"Error": "Such part does not exist"}), 404

#Updating a Single part
@inventory_bp.route("/<int:part_id>", methods=['PUT'])
def update_customer(part_id):
    part = db.session.get(Inventory, part_id)#update the customer based on their id
    if not part:
        return jsonify({"Error": "Sorry, part does not exist"}), 404 #make sure the customer exist
    
    try:
        part_data = inventoryschema.load(request.json) #load the request making sure it matches the schema
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in part_data.items(): #Go through every customer info
        setattr(part, key, value) #Update the specific infor you want to
    
    db.session.commit() #commit your request
    return inventoryschema.jsonify(part) 
    
#Delete a part
@inventory_bp.route("/<int:inventory_id>", methods=['DELETE'])
def delete_part(inventory_id):
    inventory_data = db.session.get(Inventory, inventory_id) #getting that specific customer
    if not inventory_data:
        return jsonify({"Error":"Inventory not found"}), 404
    
    db.session.delete(inventory_data)
    db.session.commit()
    return jsonify({"Message": f"Inventory id: {inventory_id}, successfully deleted"})


    
