from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    def test_it_works_using_team_access(self):
       url = "/checks/add/"

       # Logging in as bob, not alice. Bob has team access so this
       # should work.
       self.client.login(username="bob@example.org", password="password")
       r = self.client.post(url)

       c = Check.objects.get()
       self.assertEqual(c.user, self.alice)
       self.assertRedirects(r, "/checks/")
