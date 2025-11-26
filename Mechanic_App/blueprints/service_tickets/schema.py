from Mechanic_App.models import Service_Tickets, db
from Mechanic_App.extensions import ma

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Tickets
        include_fk = True          # this allow the foreign key to work
        include_relationships = True  # allow the relationships to work
        load_instance = False
        exclude = ("customer_service",) #This means you don't have to add all customer service info when testing 
        sqla_session = db.session 
ticketschema = TicketSchema()
tickets_schema = TicketSchema(many = True)