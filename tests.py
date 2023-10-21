import unittest
import requests
import json
from app import app


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_create_value(self):
        data = {'key': 'test_key', 'value': 'test_value'}
        response = self.app.post('/create', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['message'], 'Value created successfully')

    def test_update_value(self):
        # Перед обновлением значения, создаем его
        data = {'key': 'test_key', 'value': 'test_value'}
        self.app.post('/create', data=json.dumps(data), content_type='application/json')

        # Обновляем значение
        update_data = {'key': 'test_key', 'new_value': 'updated_value'}
        response = self.app.put('/update', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['message'], 'Value updated successfully')

    def test_read_value(self):
        # Перед чтением значения, создаем его
        data = {'key': 'test_key', 'value': 'test_value'}
        self.app.post('/create', data=json.dumps(data), content_type='application/json')

        # Чтение значения
        response = self.app.get('/read/test_key')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['key'], 'test_key')
        self.assertEqual(response_data['value'], 'test_value')


if __name__ == '__main__':
    unittest.main()
