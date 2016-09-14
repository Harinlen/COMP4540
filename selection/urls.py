from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.start_single_choices, name='start_single_choices'),
        url(r'^single$', views.start_single_choices, name='start_single_choices'),
        url(r'^multiple$', views.start_multiple_choices, name='start_single_choices'),
        url(r'^sendngen$', views.sendngen, name='sendngen'),
]
