from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class SendAlertsTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        
        self.assertEqual(result, True)

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        self.assertEqual(set(names), set(handled_names))

    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")
        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        
        check.save()

        self.assertTrue(Command().handle_one(check))

    def test_it_handles_nag_interval(self):
        check = Check(user=self.alice, status="up")
        # 1 day 1 hour 30 minutes after ping the check is in nag mode:
        check.last_ping = timezone.now() - timedelta(days=1, hours=1, minutes=30)
        check.nag_mode = True
        
        check.save()

        self.assertTrue(Command().handle_one(check))
