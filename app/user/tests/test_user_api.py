from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """helper function to create a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the User's _public_ API, _public_ means accessable without login"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        """Test creating a user with valid payload is successful"""
        # prepare
        payload = {
            'email': 'dummy.user@demo.org',
            'password': 'dummy-secret-pw',
            'name': 'Dummy User'
        }
        # run
        resp = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**resp.data)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', resp.data)
        self.assertTrue(user.check_password(payload['password']))

    def test_create_existant_user_fails(self):
        """Assert that trying to create an existing user fails"""
        # prepare
        payload = {
            'email': 'dummy.user@demo.org',
            'password': 'dummy-secret-pw',
            'name': 'Dummy User'
        }
        create_user(**payload)  # ensure the user is already created
        # run - attempt to re-create user via API
        resp = self.client.post(CREATE_USER_URL, payload)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_to_short_fails(self):
        """Assert that create user fails, if password is less than 6 chars"""
        # prepare
        payload = {
            'email': 'dummy.user@demo.org',
            'password': 'pw123',
            'name': 'Dummy User'
        }
        # run
        resp = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.filter(
            email=payload['email']
        )
        # assert
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user.exists())
