from Mechanic_App.models import Mechanics
from Mechanic_App.extensions import ma

#Create the mechanic 
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
mechanicschema = MechanicSchema()
mechanics_schema = MechanicSchema(many = True)
login_schema = MechanicSchema(exclude=['name', 'phone', 'salary'])