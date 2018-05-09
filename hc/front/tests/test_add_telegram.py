from hc.api.models import Check
from hc.test import BaseTestCase
from hc.front.views import add_telegram


class ChecksTestCase(BaseTestCase):

    def setUp(self):
        super(ChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alice Was Here")
        self.check.save()

    def test_telegram_url_works(self):
        """Tests whether the add telegram url works"""

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/integrations/add_telegram/")

        self.assertEqual(response.status_code, 200)

    def test_add_chat_id_works(self):
        """Tests whether the add telegram url works"""
        form = {"kind": "telegram", "value": "589607869"}
        url = "/integrations/add/"
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post("/integrations/add_telegram/", form)
        self.assertEqual(response.status_code, 200)
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")