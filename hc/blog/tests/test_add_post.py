from django.test import TestCase


from hc.test import BaseTestCase
from hc.blog.models import Category, Post


class BlogTestCase(BaseTestCase):

    def test_add_post(self):
        """Tests whether the add post works"""

        self.client.login(username="alice@example.org", password="password")

        form = {"title": "Death", "category": "life", "description":"deadly"}
        url = "/blog/add_post/"
        response = self.client.post(url, form)

        self.assertRedirects(response, "/blog/")

        self.assertEqual(response.status_code, 302)

        self.client.logout()
