from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):    # runs before any test
        # create a super- and a regular user
        self.admin_user = get_user_model().objects.create_superuser(
            'dummy.admin@demo.org',
            'dummy-secret-pw'
        )
        self.simple_user = get_user_model().objects.create_user(
            'dummy.user@demo.org',
            'dummy-secret-pw'
        )
        # prepare superuser to be logged in
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_user_listed(self):
        """test that a test user gets listed on admin's user page"""
        # run
        url = reverse('admin:core_user_changelist')
        resp = self.client.get(url)
        # assert
        self.assertContains(resp, self.simple_user.email)
        self.assertContains(resp, self.simple_user.name)
