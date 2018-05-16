from django.test import TestCase

from taggit.models import Tag
from hc.test import BaseTestCase
from hc.blog.models import Category, Post


class BlogTestCase(BaseTestCase):

    def test_add_post(self):
        """Tests whether the posts can be filtered by category"""

        self.client.login(username="alice@example.org", password="password")

        form = {"title": "Death", "category": "life", "description":"deadly"}
        url = "/blog/add_post/"
        self.client.post(url, form)

        tag_id = Tag.objects.all()[0].id

        #view post
        url = "/blog/"+ str(tag_id) + "/posts/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

        self.client.logout()
