from django.test import TestCase
from app.calc import add

class CalcTests(TestCase):

    def test_add_numbers(self):
        """test add() function, two numbers are added correctly"""
        self.assertEqual(add(3, 8), 11);

