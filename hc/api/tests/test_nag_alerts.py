from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase


class NagAlertsTestCase(BaseTestCase):

    def test_it_handles_nag_interval(self):
        check = Check(user=self.bob, status="up")
        check.timeout = timedelta(minutes=1)
        check.grace = timedelta(minutes=1)
        check.nag_interval = timedelta(minutes=1)
        check.last_ping = timezone.now() - timedelta(minutes=3)
        check.nag_mode = True
        
        check.save()

        self.assertTrue(Command().handle_one(check))
