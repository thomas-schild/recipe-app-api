from django.test import TestCase
from app.calc import add, subtract

class CalcTests(TestCase):

    def test_add_numbers(self):
        """test add(a,b) function, numbers a and b are added correctly"""
        self.assertEqual(add(3, 8), 11);

    def test_subtract_numbers(self):
        """test subtract(a,b) function, where a gets subtracted from b and assert result is correct"""
        self.assertEqual(subtract(3, 11), 8);