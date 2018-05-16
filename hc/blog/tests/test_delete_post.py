from django.test import TestCase


from hc.test import BaseTestCase
from hc.blog.models import Category, Post


class BlogTestCase(BaseTestCase):

    def test_delete_post(self):
        """Test whether delete works"""

        self.client.login(username="alice@example.org", password="password")

        #create post
        form = {"title": "Death", "category": "life", "description":"deadly"}
        url = "/blog/add_post/"
        self.client.post(url, form)

        post_id = Post.objects.all()[0].id

        #delete post
        url = "/post/"+ str(post_id) + "/delete/"
        response = self.client.get(url)

        self.assertRedirects(response, "/blog/")

        self.assertEqual(response.status_code, 302)

        self.client.logout()






