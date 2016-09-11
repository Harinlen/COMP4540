from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.start_single_choices, name='start_single_choices'),
        url(r'^sendngen$', views.sendngen, name='sendngen'),
]
