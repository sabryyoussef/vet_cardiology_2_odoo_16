# File: /home/user2/odoo16/odoo16/custom_addons/cardiology_sc/tests/test_cardiology_controller.py
import unittest
from odoo.tests.common import HttpCase


class TestCardiologyController(HttpCase):

    def test_health_check(self):
        url = '/cardiology_sc/api/health'
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200, 'Expected HTTP status code 200')
        self.assertEqual(response.json(), {'status': 'ok', 'message': 'Cardiology Controller is up and running'},
                         'Unexpected API response')


if __name__ == '__main__':
    unittest.main()
