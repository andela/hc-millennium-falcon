from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase
from django.urls import reverse

class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_redirect_on_login(self):
        """test if page redirects if registered user retries to login"""        
        url = reverse('hc-check-token', args=['alice', 'secret-token'])
        response = self.client.post(url)
        self.assertRedirects(response, "/checks/")

        newurl = self.client.post(url)
        self.assertRedirects(newurl, '/checks/')

    def test_redirect_on_bad_token(self):
        """test if page redirects on login with bad token"""
        token = self.client.post('/accounts/check_token/alice/invalid-token/')
        self.assertRedirects(token, '/accounts/login/')
