from Mechanic_App.models import Inventory
from Mechanic_App.extensions import ma

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
inventoryschema = InventorySchema()
inventorys_schema = InventorySchema(many = True)