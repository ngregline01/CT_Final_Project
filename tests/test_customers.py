from Mechanic_App import create_app
from Mechanic_App.models import db, Customers
import unittest
from Mechanic_App.utils.util import encode_token

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.mechanics_shop = create_app("TestingConfig")
        self.customer = Customers(name="John Doe", 
        email="johnd@gmail.com", phone="111-111-1111", password="john231")
        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            self.token = encode_token(1)
        self.client = self.mechanics_shop.test_client()

#Valid create test case
    def test_create_customer(self):
        customer_payload = {
            "name": "Jane Doe",
            "email": "jane@gmail.com",
            "phone": "000-000-0000",
            "password": "jane123!"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['email'], "jane@gmail.com")

#Invalid create test case
    def test_invalid_creation(self):
        customer_payload = {
            "name": "Jane Doe",
            "phone": "000-000-0000",
            "password": "jane123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

#Valid login test case
    def test_login_customer(self):
        credentials = {
            "email": "johnd@gmail.com",
            "password": "john231"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'Success')
        return response.json['token']

#Invalid login test case
    def test_invalid_login(self):
        credentials = {
            "email": "2email@gmail.com",
            "password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Message'], 'Invalid email or password')

#Valid get customers test case
    def test_get_customers(self):
        self.mechanics_shop = create_app("TestingConfig")
        self.client = self.mechanics_shop.test_client()

        #Create a dataset to practice or simulate expected test outcomes
        customers_payload = [
            {"name": "Alice Johnson", "email": "alice@example.com", "phone": "111-111-1112", "password": "Alice123!"},
            {"name": "Bob Smith", "email": "bob@example.com", "phone": "222-222-2222", "password": "Bob123!"},
            {"name": "Charlie Brown", "email": "charlie@example.com", "phone": "333-333-3333", "password": "Charlie123!"}
        ]

        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()  # fresh DB for test
            for c in customers_payload: #loop through the list
                customers = Customers(**c) #every customer will be newly created
                db.session.add(customers) #the customers are added to the session
            db.session.commit()

        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)  # matches customers inserted
        self.assertEqual(response.json[2]['email'], "charlie@example.com") #test one of it

#Valid get single customer
    def test_get_customer(self):
        self.mechanics_shop = create_app("TestingConfig")
        self.client = self.mechanics_shop.test_client()

        customer_data = {
            "name": "Eliza Weah",
            "email": "eweah@gmail.com",
            "phone": "888-888-8888",
            "password": "eweah88"
        }

        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()
            customer = Customers(**customer_data)
            db.session.add(customer)
            db.session.commit()
            customer_id = customer.id #get the generated id for the user

        response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "eweah@gmail.com")

#Invalid get single customer
    def test_invalid_get_customer(self):
        self.mechanics_shop = create_app("TestingConfig")
        self.client = self.mechanics_shop.test_client()

        customer_data = {
            "name": "Elijah Weah",
            "email": "elweah@gmail.com",
            "phone": "881-888-8888",
            "password": "eweah88"
        }

        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()
            customer = Customers(**customer_data)
            db.session.add(customer)
            db.session.commit()
            customer_id = 9999 #get the generated id for the user

        response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], "Customer does not exist")

    # Valid case for updating test case
    def test_update_customer(self):
        update_payload = {
            "name": "Mathew Wreh",
            "email": "",
            "phone": "",
            "password": ""
        }

        # Put the auth because the route has token
        headers = {
            'Authorization': "Bearer " + self.test_login_customer() 
        }

        # Make sure to include headers
        response = self.client.put('/customers/', json=update_payload, headers=headers)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Mathew Wreh")
        self.assertEqual(response.json['email'], "johnd@gmail.com")

# Invalid case for updating test case
    def test_invalid_update_customer(self):

        # Put the auth because the route has token
        headers = {
            'Authorization': "Bearer " + self.test_login_customer()
        }

        with self.mechanics_shop.app_context():
            db.drop_all() #The customer to update is drop therefore does not exist
            db.create_all()

        # Make sure to include headers
        response = self.client.put('/customers/', json={"name": "Name"}, headers=headers)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], "Sorry, customer does not exist")

#Valid test case for deleting a customer
    def test_delete_customer(self):
        headers = {
            'Authorization': "Bearer " + self.test_login_customer()
        }

        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)