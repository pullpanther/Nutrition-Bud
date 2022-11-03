import unittest

from tests.run import app

intake_record = {
    "userId": "11",
    "mealId": "122",
    "portionSize": 2,
}


class IntakeTest(unittest.TestCase):
    def test_get_all_intakes(self):
        tester = app.test_client(self)
        response = tester.get('intakes/all', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_get_intakes_by_user_id_today(self):
        tester = app.test_client(self)
        response = tester.get('intakes/today', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_post_intake(self):
        tester = app.test_client(self)
        response = tester.get('intakes/today', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()