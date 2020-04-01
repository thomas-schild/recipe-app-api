from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is success"""
        # setup / prepare
        testEmail = 'dummy.user@demo.org'
        testPasswd = 'dummy-secret-pw'
        # run
        user = get_user_model().objects.create_user(
            email=testEmail,
            password=testPasswd
        )
        # assert
        self.assertEqual(user.email, testEmail)
        self.assertTrue(user.check_password(testPasswd))
