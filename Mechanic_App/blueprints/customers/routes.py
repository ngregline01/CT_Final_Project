#blueprint/customer/routes
from . import customers_bp # The "." was used because route and init are in the same folder
from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from Mechanic_App.blueprints.customers.schema import customers_schema, customerschema, login_schema
from Mechanic_App.models import Customers, db
from Mechanic_App.extensions import limiter, cache
from Mechanic_App.utils.util import token_required, encode_token
from pydoc import pager

@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #make a query to see if the customer trying to login is in your databas
    query = select(Customers).where(Customers.email==email)
    customer = db.session.execute(query).scalars().first()

    #Check if said customer exist and if their password matches the one being entered by the user
    if customer and customer.password == password:
        token = encode_token(customer.id)
        #give the user a response
        response = {
            "response":"Success",
            "Message": "Successfully Logged In",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"Message": "Invalid email or password"}), 400

#Create a Customer
@customers_bp.route( "/", methods=['POST'])
#@limiter.limit("2 per day")
#@cache.cached(timeout=30)
def create_customer():
    try: #put validation on the customer info that is being fire or sent to the server
        customer_data = customerschema.load(request.json)#we use the schema so validation can use on the data seamlessly
    except ValidationError as e:
        return jsonify(e.messages), 400 #if the data does not match the expected pattern then it is return as a bad request

    query = select(Customers).where(Customers.email==customer_data['email']) #this to find a specific customer that aligns with the email because this email is actually unique too
    existing_customer = db.session.execute(query).scalars().all() #select all the info that matches the query
    if existing_customer:
        return jsonify({"Error": "Customer already exist"}), 400 #error because the customer exist
    new_customer = Customers(**customer_data) #destructure the customer data to create a new_customer
    db.session.add(new_customer) #add the new customer to the session
    db.session.commit() #commit it
    return customerschema.jsonify(new_customer), 201 #return the new_customer, using customer schema

#Retreive all Customers
@customers_bp.route("/", methods=['GET'] )
#@cache.cached(timeout=30)
def get_customers():
    #query = select(Customers) #This is used to get all of the customers
    #customers = db.session.execute(query).scalars().all() #then you get all the customers that match the customers
    #return customers_schema.jsonify(customers), 200 #this display the customers

    #Pagination is applied below
    try:
        page = int(request.args.get('page'))
        per_page =int(request.args.get('per_page'))
        query = select(Customers)
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        #if the pagination does not work for whatever reason, it gives you the default 
        query = select(Customers) #This is used to get all of the customers
        customers = db.session.execute(query).scalars().all() #then you get all the customers that match the customers
        return customers_schema.jsonify(customers), 200 #this display the customers


#Retrieve a Single Customer
@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    #using the get method with path parameter
    customer_data = db.session.get(Customers, customer_id) #getting the exact customer with specific id using path parameter
    if customer_data:
        return customerschema.jsonify(customer_data)
    return jsonify({"message": "Customer does not exist"}), 404

# Updating a Single Customer
@customers_bp.route("/", methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"message": "Sorry, customer does not exist"}), 404
    
    try:
        customer_data = customerschema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Only update fields that are not empty strings
    for key, value in customer_data.items():
        if value not in ("", None):
            setattr(customer, key, value)
    
    db.session.commit()
    return customerschema.jsonify(customer)

    
#Delete a Customer
@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer_data = db.session.get(Customers, customer_id) #getting that specific customer
    if not customer_data:
        return jsonify({"Error":"Customer not found"}), 404
    
    db.session.delete(customer_data)
    db.session.commit()
    return customerschema.jsonify({"Message": f"Customer id: {customer_id}, successfully deleted"}), 200

