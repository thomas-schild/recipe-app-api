from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(
        email='dummy.user@demo.org',
        password='dummy-secret-pw'
     ):
    """helper function to create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        # setup / prepare
        testEmail = 'dummy.user@demo.org'
        testPasswd = 'dummy-secret-pw'
        # run
        user = sample_user(
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
        testEmail = '{}@{}'.format(
            testEmailUser,
            testEmailDomain
        )
        # run
        user = sample_user(email=testEmail)
        # assert email domain part is on lower case
        normalizedEmail = '{}@{}'.format(
            testEmailUser,
            testEmailDomain.lower()
        )
        self.assertEqual(user.email, normalizedEmail)

    def test_create_user_fails_for_invalid_email(self):
        """Assert that an error is raised if no valid email \
        is provided when user is created"""
        # assert, when run
        with self.assertRaises(ValueError):
            sample_user(email=None)

    def test_create_superuser(self):
        """Test creating a superuser is successful"""
        # run
        superuser = get_user_model().objects.create_superuser(
            'dummy.admin@demo.org',
            'dummy-secret-pw'
        )
        # assert
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_tag_str(self):
        """Test a tag's string representation"""
        # run - create a Tag
        tag = models.Tag.objects.create(
            name='Test Tag',
            user=sample_user(),
        )
        # assert
        self.assertEqual(str(tag), tag.name)
