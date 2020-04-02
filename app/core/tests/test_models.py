from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
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

    def test_on_create_user_email_is_normalized(self):
        """Assert that email is normalized when user is created"""
        # setup / prepare
        testEmailUser = 'dUmmy.User'
        testEmailDomain = 'dEmo.Org'
        testPasswd = 'dummy-secret-pw'
        # run
        user = get_user_model().objects.create_user(
            email='{}@{}'.format(testEmailUser, testEmailDomain),
            password=testPasswd
        )
        # assert email domain part is on lower case
        normalizedEmail = '{}@{}'.format(
            testEmailUser,
            testEmailDomain.lower()
        )
        self.assertEqual(user.email, normalizedEmail)

    def test_create_user_failes_for_invalid_email(self):
        """Assert that an error is raised if no valid email \
        is provided when user is created"""
        # setup
        testEmail = None
        testPasswd = 'dummy-secret-pw'
        # assert, when run
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=testEmail,
                password=testPasswd
            )
        