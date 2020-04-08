from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
SELF_URL = reverse('user:self')


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
            'password': 'dummy-secret-pw',
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
            'password': 'dummy-secret-pw',
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

    def test_retrieve_user_unauthorized_fails(self):
        """Assert that authentication is required to access a user's profile"""
        # run
        resp = self.client.get(SELF_URL)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the User's _private_ API,
        _private_ means authentication is required"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='dummy.user@demo.org',
            password='dummy-secret-pw',
            name='Dummy Test User'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile_success(self):
        """Test that user can access his profile"""
        # run
        resp = self.client.get(SELF_URL)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_method_for_user_profile_fails(self):
        """Assert that POST method is not allowed on user's profile"""
        # prepare
        payload = {
            'email': 'dummy.user@demo.org',
            'password': 'dummy-secret-pw',
            'name': 'Dummy User updated'
        }
        # run
        resp = self.client.post(SELF_URL, payload)
        # assert
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_success(self):
        """Test updating a user profile for authenticated user"""
        # prepare
        payload = {
            'email': 'dummy.user@demo.org',
            'password': 'dummy-secret-pw',
            'name': 'Dummy User updated'
        }
        # run
        resp = self.client.put(SELF_URL, payload)
        self.user.refresh_from_db()
        # assert
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))

    def test_patch_user_profile_success(self):
        """Test patching a user profile for authenticated user"""
        # prepare
        prev_email = self.user.email
        payload = {
            # no password or email provided here, only name is patched
            'name': 'Dummy User updated'
        }
        # run
        resp = self.client.patch(SELF_URL, payload)
        self.user.refresh_from_db()
        # assert
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.email, prev_email)
