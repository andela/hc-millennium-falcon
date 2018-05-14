from django.conf.urls import include, url

from hc.help import views


urlpatterns = [
    url(r'^faq/$', views.faq, name="hc-faq"),
    url(r'^videos/$', views.videos, name="hc-videos")
]
