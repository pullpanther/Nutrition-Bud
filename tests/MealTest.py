import json
import unittest
from tests.run import app

meal_body = {
    'id': '0',
    'name': 'Egg',
    'portion': 100,
    'portionType': 'g',
    'calories': 155,
    'fat': 11,
    'carbohydrates': 1.1,
    'protein': 13,
}

class IntakeTest(unittest.TestCase):
    def test_get_all_meals(self):
        tester = app.test_client(self)
        response = tester.get('meals', content_type='html/text')
        print(response.json)
        self.assertEqual(response.status_code, 200)


    def test_get_meal_by_id(self):
        tester = app.test_client(self)
        response = tester.get('meals/1', content_type='html/text')
        print(response.json)
        self.assertEqual(response.status_code, 200)


    def test_create_meals(self):
        tester = app.test_client(self)
        response = tester.post('/meals', content_type='application/json', data=json.dumps(meal_body))
        print(response.json)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()