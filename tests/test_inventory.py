from Mechanic_App import create_app
from Mechanic_App.models import db, Inventory
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.mechanics_shop = create_app("TestingConfig")
        self.part = Inventory(name="tester", price="15.00")
        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.part)
            db.session.commit()
        self.client = self.mechanics_shop.test_client()

    #Valid to create part
    def test_create_part(self):
        part_payload = {
            "name": "Brake pads",
            "price": "75.00"
        }

        response = self.client.post('/inventory/', json=part_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Brake pads")

    #InValid to create part
    def test_invalid_create_part(self):
        part_payload = {
            "name": "tester",
            "price": "15.00"
        }

        response = self.client.post('/inventory/', json=part_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Message'], "part already exist")

    #Valid to get parts
    def test_get_part(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], "tester")

    #Valid get single part
    def test_get_part(self):
        self.mechanics_shop = create_app("TestingConfig")
        self.client = self.mechanics_shop.test_client()

        part_data = {
            "name": "Tires",
            "price": "40.00"
        }

        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()
            part = Inventory(**part_data)
            db.session.add(part)
            db.session.commit()
            part_id = part.id #get the generated id for the user

        response = self.client.get(f'/inventory/{part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Tires")

#Valid update case
    def test_update_part(self):
        # First create the part so there is something to update
        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()

            part = Inventory(
                name="Old Wipers",
                price="10.00"
            )
            db.session.add(part)
            db.session.commit()
            part_id = part.id  

        # Update payload
        part_payload = {
            "name": "Wipers",
            "price": "15.00"
        }

        # Now update the existing part using PUT /inventory/<id>
        response = self.client.put(f'/inventory/{part_id}', json=part_payload)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Wipers")
        self.assertEqual(response.json['price'], "15.00")

    # Delete test case
    def test_delete_inventory(self):
        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()

            part = Inventory(
                name="Brake Pad",
                price="25.00"
            )
            db.session.add(part)
            db.session.commit()
            part_id = part.id

        response = self.client.delete(f'/inventory/{part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['Message'],  f"Inventory id: {part_id}, successfully deleted")
