from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from Mechanic_App.models import Service_Tickets, Customers, Mechanics, ServicePart, Inventory, db
from Mechanic_App.blueprints.service_tickets.schema import ticketschema, tickets_schema
from . import tickets_bp
from Mechanic_App.extensions import limiter, cache
from Mechanic_App.utils.util import token_required

@tickets_bp.route("/", methods=['POST'])
def create_services():
    try:
        # Load JSON into a Service_Tickets object, ignore relationships for now
        service_data = ticketschema.load(
            request.json, 
            partial=("mechanic_services", "customer_service")
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check if service with same VIN already exists
    existing_service = db.session.execute(
        select(Service_Tickets).where(Service_Tickets.vin == service_data['vin'])
    ).scalars().all()

    if existing_service:
        return jsonify({"Error": "Service already exists"}), 400

    # Fetch existing customer
    customer_id = request.json.get("customer_id")
    customer = db.session.query(Customers).get(customer_id)
    if not customer:
        return jsonify({"Error": "Customer does not exist"}), 400

    # Fetch existing mechanics
    mechanic_ids = request.json.get("mechanic_services", [])
    mechanics = []
    if mechanic_ids:
        mechanics = db.session.query(Mechanics).filter(Mechanics.id.in_(mechanic_ids)).all()
        if len(mechanics) != len(mechanic_ids):
            return jsonify({"Error": "One or more mechanic IDs do not exist"}), 400

    # Create new service ticket and link customer + mechanics
    new_service = Service_Tickets(**service_data)
    new_service.customer_service = customer
    new_service.mechanic_services = mechanics  # link existing mechanics

    db.session.add(new_service)
    db.session.commit()

    return ticketschema.jsonify(new_service), 201

#Retrieve all tickets
@tickets_bp.route("/", methods=['GET'])
#@cache.cached(timeout=30)
def get_services():
    query = select(Service_Tickets)
    services = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(services)

#Adds a relationship between a service and the mechanic
@tickets_bp.route("/<int:ticket_id>/assign-mechanic/<mechanic_id>", methods=['PUT'])
#@limiter.limit("3 per hour")
def assigning_mechanics(ticket_id, mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    service = db.session.get(Service_Tickets, ticket_id)
    if not mechanic:
        return jsonify({"Error": "Mechanic does not exist"}), 404
    if not service:
        return jsonify({"Error": "Sorry, service does not exist"}), 404
    
    if mechanic not in service.mechanic_services:
        service.mechanic_services.append(mechanic)
        db.session.commit()
        return jsonify({"Message": "Mechanic successfully added"}), 201
    else:
        return jsonify({"Error": "Unable to add mechanic"})

#Removes a relationship between a service and the mechanic
@tickets_bp.route("/<ticket_id>/remove-mechanic/<mechanic_id>", methods=['PUT'])
#@limiter.limit("2 per hour")
def removing_mechanics(ticket_id, mechanic_id):
    service = db.session.get(Service_Tickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"Error": "Mechanic does not exist"}), 404
    if not service:
        return jsonify({"Error": "Sorry, service does not exist"}), 404
    
    if mechanic in service.mechanic_services:
        service.mechanic_services.remove(mechanic)
        db.session.commit() #Always remember to commit when you change something to the database
        return jsonify({"Message": "Successfully remove mechanic"}), 200
    else:
        return jsonify({"Error": "Unable to delete mechanic"}), 400
    

#Retrieve service tickets based on a customer
@tickets_bp.route("/my-tickets", methods=['GET'])
@token_required
def get_customer_tickets(customer_id):
    #Find all service tickets that belongs to this customer
    tickets = db.session.query(Service_Tickets).filter_by(customer_id=customer_id).all()

    #gets and return the ticket
    if tickets:
        return tickets_schema.jsonify(tickets)
    else:
        return jsonify({"Message": "No tickets found for this customer."}), 400


#Add parts to a service ticket
@tickets_bp.route("/<int:ticket_id>/add-part/<inventory_id>", methods=["POST"])
def add_part(ticket_id, inventory_id):
    ticket = db.session.get(Service_Tickets, ticket_id)
    part = db.session.get(Inventory, inventory_id)
    if not ticket or not part:
        return jsonify({"Message": "Missing ticket_id or part_id"}), 400
    
    #Add a quantity based on the many-many model
    data = request.get_json()
    quantity = data.get("quantity_used", None)
    if quantity is None:
        return jsonify({"Message": "A quantity is required"}), 400
    
    #create the association for both
    service_inventory = ServicePart(
        ticket_id = ticket_id,
        inventory_id = inventory_id,
        quantity_used = quantity
    )

    db.session.add(service_inventory)
    db.session.commit()

    return jsonify({
        "message": "Part added to service ticket",
        "ticket_id": ticket_id,
        "inventory_id": inventory_id,
        "quantity_used": quantity
    }), 201


