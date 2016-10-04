from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.start_question, name='start_question'),
        url(r'^sendquestionresult$', views.send_question_result, name='send_question_result'),
        url(r'^initialtest$', views.start_initial_test, name='start_initial_test'),
        url(r'^multiple$', views.start_multiple_choices, name='start_multiple_choices'),
        url(r'^nthiteration$', views.start_multiple_choices, name='start_multiple_choices'),
        url(r'^generateiteration$', views.generate_iteration_images, name='generate_iteration_images'),
        url(r'^saveinitial$', views.send_initial, name='send_initial'),
]
