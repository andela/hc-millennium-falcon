from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone
from hc.front.views import my_failed_checks


class MyFailedChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyFailedChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alice Was Here")
        self.check.save()

    def test_failed_checks_url_works(self):
        """Tests whether the failed_checks url works"""

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/failed_checks/")

        self.assertEqual(response.status_code, 200)

    def test_only_failed_checks_are_returned(self):
        """Tests whether only checks with status down are returned"""

        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "down"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/failed_checks/")
        self.assertContains(response, "Alice Was Here")

    def test_up_checks_not_returned(self):
        """Tests whether checks with status up are not returned"""
        
        self.check.last_ping = timezone.now()
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/failed_checks/")
        self.assertNotIn( "Alice Was Here", response)

    def test_grace_checks_not_returned(self):
        """Tests whether checks with status grace are not returned"""

        self.check.last_ping = timezone.now() - td(days=1, minutes=30)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/failed_checks/")
        self.assertNotIn( "Alice Was Here", response)


