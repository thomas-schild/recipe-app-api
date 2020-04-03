import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django Command to pause execution until the database is ready"""

    def handle(self, *arg, **options):
        db_connection = None
        self.stdout.write("waiting for database...")
        while not db_connection:
            try:
                db_connection = connections['default']
            except OperationalError:
                self.stdout.write("database not ready, waiting for 1s ...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("database is ready now"))
