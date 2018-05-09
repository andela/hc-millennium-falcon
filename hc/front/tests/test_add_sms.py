from hc.api.models import Check
from hc.test import BaseTestCase


class MyFailedChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyFailedChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alice Was Here")
        self.check.save()

    def test_sms_url_works(self):
        """Tests whether the add telegram url works"""

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/integrations/add_sms/")

        self.assertEqual(response.status_code, 200)

    def test_add_chat_phonenumber_works(self):
        """Tests whether the add telegram url works"""
        form = {"kind": "sms", "value": "+256781723456"}
        url = "/integrations/add/"
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post("/integrations/add_sms/", form)
        self.assertEqual(response.status_code, 200)
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")