from Mechanic_App import create_app
from Mechanic_App.models import db, Mechanics, Service_Tickets
import unittest
from Mechanic_App.utils.util import encode_token
from datetime import date



class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.mechanics_shop = create_app("TestingConfig")
        self.mechanic = Mechanics(name="Johnetta Doe", 
        email="jd@gmail.com", phone="222-111-1111", salary="1000.00", password="jetta231")
        with self.mechanics_shop.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
            self.token = encode_token(1)
        self.client = self.mechanics_shop.test_client()

#Valid to create mechanic
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "email": "john@email.com",
            "phone": "222-222-2222",
            "salary": "10000.00",
            "password": "john231"
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

#Invalid to create
    def test_invalid_create_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "phone": "222-222-2222",
            "salary": "10000.00",
            "password": "john231"
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ["Missing data for required field."])

#Valid to login mechanic
    def test_login_mechanic(self):
        credentials = {
            "email": "jd@gmail.com",
            "password": "jetta231"
        }

        response = self.client.post('/mechanics/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], "Success")
        return response.json['token']

#Invalid to login mechanic
    def test_invalid_login_mechanic(self):
        credentials = {
            "email": "2jd@gmail.com",
            "password": "jetta231"
        }

        response = self.client.post('/mechanics/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Message'], "Invalid email or password")

#Valid to get mechanics
    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], "Johnetta Doe")

#Valid to update mechanics
    def test_update_mechanics(self):

        update_payload = {
            "name": "Mary Doe",
            "email": "jd@gmail.com",
            "phone": "222-111-1111",
            "salary": "1000.00",
            "password": "jetta231"
        }

        headers = {
            'Authorization': "Bearer " + self.test_login_mechanic()
        }


        response = self.client.put('/mechanics/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Mary Doe")
        self.assertEqual(response.json['email'], "jd@gmail.com")

#Delete test case
    def test_delete_mechanic(self):
        headers = {
            "Authorization": "Bearer " + self.test_login_mechanic()
        }
        response = self.client.delete('/mechanics/', headers=headers)
        self.assertEqual(response.status_code, 200)

#Popular mechanic
    def test_get_mechanics(self):
        response = self.client.get('/mechanics/popular')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], "Johnetta Doe")