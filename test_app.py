import unittest
from app import app, db
from models import Brand, Model

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_get_brands(self):
        # Asegúrate de que la base de datos esté vacía al principio
        response = self.client.get('/brands/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_add_brand(self):
        response = self.client.post('/brands/', json={"name": "Test Brand"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Test Brand')

    def test_add_duplicate_brand(self):
        self.client.post('/brands/', json={"name": "Test Brand"})
        response = self.client.post('/brands/', json={"name": "Test Brand"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Brand name already exists", response.json['error'])

    def test_add_model_to_brand(self):
        self.client.post('/brands/', json={"name": "Test Brand"})
        response = self.client.post('/brands/1/models', json={"name": "Test Model", "average_price": 150000})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Test Model')

    def test_update_model(self):
        self.client.post('/brands/', json={"name": "Test Brand"})
        self.client.post('/brands/1/models', json={"name": "Test Model", "average_price": 150000})
        response = self.client.put('/models/1', json={"average_price": 200000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['average_price'], 200000)

    def test_get_models_with_filter(self):
        self.client.post('/brands/', json={"name": "Test Brand"})
        self.client.post('/brands/1/models', json={"name": "Test Model 1", "average_price": 150000})
        self.client.post('/brands/1/models', json={"name": "Test Model 2", "average_price": 250000})
        response = self.client.get('/models?greater=100000&lower=200000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Test Model 1')

if __name__ == "__main__":
    unittest.main()