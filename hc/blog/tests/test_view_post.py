from django.test import TestCase


from hc.test import BaseTestCase
from hc.blog.models import Category, Post


class BlogTestCase(BaseTestCase):

    def test_view_post(self):
        """ Test whether view post works """

        self.client.login(username="alice@example.org", password="password")

        #create post
        form = {"title": "Death", "category": "life", "description":"deadly"}
        url = "/blog/add_post/"
        self.client.post(url, form)

        post_id = Post.objects.all()[0].id

        #view post
        url = "/blog/"+ str(post_id) + "/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

        self.client.logout()





