from django.test import TestCase


from hc.test import BaseTestCase
from hc.blog.models import Category, Post


class BlogTestCase(BaseTestCase):

    def test_edit_post(self):
        """Tests whether edit post works"""

        self.client.login(username="alice@example.org", password="password")

        #create post
        form = {"title": "Death", "category": "life", "description":"deadly"}
        url = "/blog/add_post/"
        self.client.post(url, form)

        post_id = Post.objects.all()[0].id

        #Edit post
        url = "/post/"+ str(post_id) +"/edit/"
        form = {"title": "Good", "category": "food", "description":"Nice"}
        response = self.client.post(url, form)

        self.assertRedirects(response, "/blog/"+ str(post_id) +"/")

        self.assertEqual(response.status_code, 302)

        self.client.logout()
