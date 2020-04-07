from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


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

    def test_create_token_for_user(self):
        """Test that a token is created for a given user"""
        # prepare
        payload = {
            'email': 'dummy.user@demo.org',
            'password': 'pw123',
            'name': 'Dummy User'
        }
        # ... create a user with this payload, i.e. the 'given' user
        create_user(**payload)
        # run
        # ... use the REST-API to create a token for this payload
        resp = self.client.post(TOKEN_URL, payload)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)

    def test_create_token_with_invalid_credential_fails(self):
        """Assert that no token is granted for invalid credentials"""
        # prepare
        # ... create a 'given' user
        create_user(email='dummy.user@demo.org', password='valid')
        payload = {
            'email': 'dummy.user@demo.org',
            'password': 'invalid',
            'name': 'Dummy User'
        }
        # run
        # ... try to create a token for this invalid payload
        resp = self.client.post(TOKEN_URL, payload)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', resp.data)

    def test_create_token_without_user(self):
        """Assert that no token is granted if there is no matching user"""
        # prepare
        payload = {
            'email': 'dummy.user@demo.org',
            'password': 'invalid',
            'name': 'Dummy User'
        }
        # run
        # ... try to create a token for this payload
        resp = self.client.post(TOKEN_URL, payload)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', resp.data)

    def test_create_token_missing_fields_fails(self):
        """Assert that no token is granted for invalid credentials"""
        # prepare
        # ... create a 'given' user
        create_user(email='dummy.user@demo.org', password='valid')
        payload_incomplete = {
            'email': 'dummy.user@demo.org',
        }
        # run
        # ... try to create a token for this invalid payload
        resp = self.client.post(TOKEN_URL, payload_incomplete)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', resp.data)
