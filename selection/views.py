from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models
from selection.models import ExpResult
import hashlib

single_choice_codename = 'akatsuki'
multiple_choice_codename = 'musashi'

initial_test_maximum_radio = 7;
initial_test_image=[['static/images/1.png',
                     'static/images/2.png',
                     'static/images/3.png',
                     'static/images/4.png',
                     'static/images/5.png',
                     'static/images/6.png',
                     'static/images/7.png',
                     'static/images/8.png',
                     'static/images/9.png',
                     'static/images/10.png',
                     'static/images/11.png',
                     'static/images/12.png',
                     'static/images/13.png',
                     'static/images/14.png',
                     'static/images/15.png',
                     'static/images/16.png',
                     'static/images/17.png',
                     'static/images/18.png',
                     'static/images/19.png',
                     'static/images/20.png']];
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
    multiple_test_image=['static/images/1.png',
                  'static/images/2.png',
                  'static/images/3.png',
                  'static/images/4.png',
                  'static/images/5.png',
                  'static/images/6.png',
                  'static/images/7.png',
                  'static/images/8.png',
                  'static/images/9.png',
                  'static/images/10.png',
                  'static/images/11.png',
                  'static/images/12.png',
                  'static/images/13.png',
                  'static/images/14.png',
                  'static/images/15.png',
                  'static/images/16.png',
                  'static/images/17.png',
                  'static/images/18.png',
                  'static/images/19.png',
                  'static/images/20.png',
                  'static/images/1.png',
                  'static/images/2.png',
                  'static/images/3.png',
                  'static/images/4.png',
                  'static/images/5.png',
                  'static/images/6.png',
                  'static/images/7.png'];
    return render(request, multiple_choice_codename + '/index.html',
                  {'testList':multiple_test_image,
                   'testTitle':"'Mondrian Painting #'",
                   'testHintText':"'Choose the images you like'",
                   'testScoreHintText':"'Score the chosen images'",
                   'testDriveHintText':"'Use A(left), W(mid), D(right) to select the group contains the most image you like'",
                   'testDriveConfirmText':"'Hit the same key again to confirm, or S(back) to cancel'",
                   'testSingleIndex':1,
                   'testUIIndex':0});

def start_s_choices(request):
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
        exp_result=post_data["exp_result"];
        print(post_data["exp_result"]);
        exp_result = ExpResult(result=exp_result,
                               title=hashlib.sha512(exp_result.encode('utf-8')).hexdigest());
        exp_result.save();
        return JsonResponse({'state':'ok'});
    return start_single_choices(request);
