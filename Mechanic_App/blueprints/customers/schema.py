from Mechanic_App.models import Customers
from Mechanic_App.extensions import ma

#Creating a schema
class CustomerSchema(ma.SQLAlchemyAutoSchema): #create the schema
    class Meta: #meta class to link every thin
        model = Customers
customerschema = CustomerSchema()#use for serialization of a single customer
customers_schema = CustomerSchema(many=True) #use for serialization of multiple customers
login_schema = CustomerSchema(exclude=['name', 'phone'])