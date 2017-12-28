from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^travels/$', views.travel_list, name='travels'),
    url(r'^travel/(?P<pk>[0-9]+)/$', views.travel_detail, name='travel_detail'),
]
