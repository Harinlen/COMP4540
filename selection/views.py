from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models
from selection.models import ExpResult

single_choice_codename = 'akatsuki'

initial_test_maximum_radio = 7;
initial_test_image=[ '/static/images/1.png',
                '/static/images/2.png',
                '/static/images/3.png',
                '/static/images/4.png',
                '/static/images/5.png',
                '/static/images/6.png',
                '/static/images/7.png',
                '/static/images/8.png',
                '/static/images/9.png',
                '/static/images/10.png',
                '/static/images/11.png',
                '/static/images/12.png',
                '/static/images/13.png',
                '/static/images/14.png',
                '/static/images/15.png',
                '/static/images/16.png',
                '/static/images/17.png',
                '/static/images/18.png',
                '/static/images/19.png',
                '/static/images/20.png'];
initial_test_list=[ 0,0,0,0,
                    1,1,1,1,
                    2,2,2,2,
                    3,3,3,3,
                    4,4,4,4];
initial_test_text=['Do you like this image?',
                 'Do you like this image?',
                 'Do you like this image?',
                 'Do you like this image?',
                 'Do you like this image?',
                 'Do you like this image?',
                 'Do you like this image?',
                 'Do you like this image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?',
                 'Please indicate how much you like the image?'];
initial_test_label = [[],
                      [],
                      [],
                      [],
                      [],
                      [],
                      [],
                      [],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like'],
                      ['Dislike', 'So-so', 'Like']];

q_image = [ '/static/images/1.png'];
q_list = [2];
q_text = ['Test'];
q_label = [['Dislike', 'Normal', 'Like']];

def start_single_choices(request):
    return render(request, single_choice_codename + '/index.html',
                  {'testImage': initial_test_image,
                    'testList': initial_test_list,
                    'testHintText': initial_test_text,
                    'testLabel': initial_test_label,
                    'testRadioMaximum': initial_test_maximum_radio});

def sendngen(request):
    # Check the result.
    if(request.method=="POST"):
        post_data=request.POST;
        print(post_data["exp_result"]);
        exp_result = ExpResult(result=post_data["exp_result"],
                               title='username|date|iteration');
        exp_result.save();
        return JsonResponse({'state':'ok'});
    return start_single_choices(request);
