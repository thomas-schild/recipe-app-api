from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_while_available(self):
        """test waiting for db when db is available"""
        # prepare: mock db behavior when db is ready,
        # i.e. raise no OperationalError
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            # run
            call_command('wait_for_db')
            # assert
            self.assertEqual(gi.call_count, 1)

    # mock sleep-time, so in the test we need not to wait 5-times for 1s
    # after a failed attempt to get the db connection handler
    @patch('time.sleep', return_value=None)
    # the @patch'ed time.sleep gets passed in here as patchedTimeSleep
    # (tough not called explicitly)
    def test_wait_for_db(self, patchedTimeSleep):
        """test waiting for db"""
        # prepare: mock that trying to get the db-connection-handler
        # raised 5 time an OperationalError but is successful for the 6th time
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            # run
            call_command('wait_for_db')
            # assert
            self.assertEqual(gi.call_count, 6)
