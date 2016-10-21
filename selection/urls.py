from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.start_question, name='start_question'),
        url(r'^sendquestionresult$', views.send_question_result, name='send_question_result'),
        url(r'^sendsinglequestionresult$', views.send_single_question_result, name='send_single_question_result'),
        url(r'^sendeyetribe$', views.send_eyetribe, name='send_eyetribe'),
        url(r'^sendmultiplequestionresult$', views.send_multiple_question_result, name='send_multiple_question_result'),
        url(r'^initialtestquestion$', views.start_single_question, name='start_single_question'),
        url(r'^initialtest$', views.start_initial_test, name='start_initial_test'),
        url(r'^multiplequestion$', views.start_multiple_question, name='start_multiple_question'),
        url(r'^multiple$', views.start_multiple_choices, name='start_multiple_choices'),
        url(r'^nthiteration$', views.start_multiple_choices, name='start_multiple_choices'),
        url(r'^generateiteration$', views.generate_iteration_images, name='generate_iteration_images'),
        url(r'^saveinitial$', views.send_initial, name='send_initial'),
        url(r'^saveiteration$', views.send_iteration, name='send_iteration'),
]
