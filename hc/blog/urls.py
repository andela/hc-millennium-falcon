from django.conf.urls import url

from hc.blog import views

urlpatterns = [
    url(r'^blog/$', views.blog_posts, name="blog-view-posts"),
    url(r'^blog/(?P<pk>\d+)/$', views.post_details, name="view-post-details"),
    url(r'^blog/add_post/$', views.add_post, name="new-post"),
    url(r'^post/(?P<pk>\d+)/edit/$', views.edit_post, name="edit_post"),
    url(r'^post/(?P<pk>\d+)/delete/$', views.delete_post, name="delete_post"),
    url(r'^blog/add_category/$', views.add_category, name="new_category"),
    url(r'^blog/(?P<pk>\d+)/posts/$', views.view_category_posts, name="category_posts")
]
