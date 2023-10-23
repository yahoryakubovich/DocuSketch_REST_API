import json
import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_create_value(self):
        response = self.app.post('/create', json={'key': 'test_key', 'value': 'test_value'})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', data)
        self.assertIn('Value created successfully', data['message'])

    def test_update_value(self):
        response = self.app.put('/update', json={'key': 'nonexistent_key', 'new_value': 'updated_value'})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertIn('Key not found', data['message'])

    def test_read_value(self):
        response = self.app.get('/read/test_key')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('key', data)
        self.assertIn('value', data)
        self.assertEqual(data['key'], 'test_key')
        self.assertEqual(data['value'], 'updated_test_value')

    def test_read_nonexistent_value(self):
        response = self.app.get('/read/nonexistent_key')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertIn('Key not found', data['message'])

if __name__ == '__main__':
    unittest.main()
