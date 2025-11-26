from Mechanic_App import create_app
from Mechanic_App.models import db, Customers, Service_Tickets, Inventory, Mechanics
from datetime import date
from Mechanic_App.utils.util import encode_token
import unittest


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.mechanics_shop = create_app("TestingConfig")
        
        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()

            #create a mechanic
            mechanic = Mechanics(name="Bob", email="bob@gmail.com", phone="111-222-3333", salary="90000", password="bobpass")
            db.session.add(mechanic)
            db.session.commit()
            self.mechanic_id = mechanic.id

            # Create a customer for FK
            self.customer = Customers(
                name="John Doe",
                email="jd@gmail.com",
                phone="222-111-1111",
                password="john123"
            )
            db.session.add(self.customer)
            db.session.commit()
            self.customer_id = self.customer.id

            # Create a service ticket once, so it exists for all GET/update/delete tests
            ticket = Service_Tickets(
                customer_id=self.customer_id,
                vin="VIN00000000000001", 
                service_date=date(2024, 11, 20),
                service_desc="Oil change and tire rotation"
            )
            db.session.add(ticket)
            db.session.commit()
            self.ticket_id = ticket.id  # store the ID for later tests

            # Create inventory item
            part = Inventory(
                name="Brake Pads",
                price="75.00"
            )
            db.session.add(part)
            db.session.commit()
            self.inventory_id = part.id

        self.client = self.mechanics_shop.test_client()

#Test for getting service tickets
    def test_get_service_ticket(self):
        response = self.client.get("/service_tickets/")
        self.assertEqual(response.status_code, 200)

        tickets = response.json
        self.assertGreater(len(tickets), 0)
        self.assertEqual(tickets[0]["vin"], "VIN00000000000001")
        self.assertEqual(tickets[0]["service_desc"], "Oil change and tire rotation")

#test for creating service
    def test_create_service_ticket(self):
        payload = {
            "customer_id": self.customer_id,
            "vin": "VIN11111111111111",
            "service_date": "2024-11-21",
            "service_desc": "Brake inspection"
        }
        response = self.client.post("/service_tickets/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["vin"], "VIN11111111111111")

#Test for adding parts
    def test_add_part(self):
        payload = {"quantity_used": 2}

        response = self.client.post(
            f"/service_tickets/{self.ticket_id}/add-part/{self.inventory_id}",
            json=payload
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["ticket_id"], self.ticket_id)
        self.assertEqual(int(response.json["inventory_id"]), self.inventory_id)
        self.assertEqual(response.json["quantity_used"], 2)

#Test case for assigning mechanic
    def test_assign_mechanic(self):
        # Make request
        response = self.client.put(
            f"/service_tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["Message"], "Mechanic successfully added")

#Test case for removing mechanic
    def test_remove_mechanic(self):

        # First assign the mechanic
        assign_response = self.client.put(
            f"/service_tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}"
        )
        self.assertEqual(assign_response.status_code, 201)

        # Make request
        response = self.client.put(
            f"/service_tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["Message"], "Successfully remove mechanic")

    def test_customer_ticket(self):
        with self.mechanics_shop.app_context():
            token = encode_token(self.customer_id)
            headers = {
                "Authorization": f"Bearer {token}"
            }
        response = self.client.get("/service_tickets/my-tickets", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["vin"], "VIN00000000000001")
        
