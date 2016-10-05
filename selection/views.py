from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from . import models
from selection.models import ExpResult
from enum import Enum
from PIL import Image
from .mondrian import imageGenerator
from django.views.decorators.csrf import csrf_exempt
import os.path
import json
import hashlib

single_choice_codename = 'akatsuki'
multiple_choice_codename = 'musashi'
question_codename = 'shimakaze'

class Question_Type(Enum):
    Combo = 0;
    Text = 1;
    Slider = 2;
    Radio = 3;
    Checkbox = 4;
    SearchCombo = 5;

# Initial static 27 images genes.
imageList = [
    # 1
    [
        {'startx': '0', 'starty': '0', 'endx': '480', 'endy': '130', 'color': 'red'},
        {'startx': '0', 'starty': '130', 'endx': '280', 'endy': '480', 'color': 'yellow'},
        {'startx': '280', 'starty': '130', 'endx': '480', 'endy': '300', 'color': 'white'},
        {'startx': '280', 'starty': '300', 'endx': '480', 'endy': '480', 'color': 'blue'}
    ],

    # 2
    [
        {'startx': '0', 'starty': '0', 'endx': '100', 'endy': '320', 'color': 'red'},
        {'startx': '0', 'starty': '320', 'endx': '100', 'endy': '480', 'color': 'white'},
        {'startx': '100', 'starty': '0', 'endx': '330', 'endy': '160', 'color': 'white'},
        {'startx': '100', 'starty': '160', 'endx': '330', 'endy': '480', 'color': 'white'},
        {'startx': '330', 'starty': '0', 'endx': '480', 'endy': '230', 'color': 'blue'},
        {'startx': '330', 'starty': '230', 'endx': '480', 'endy': '480', 'color': 'yellow'}
    ],

    # 3
    [
        {'startx': '0', 'starty': '0', 'endx': '170', 'endy': '180', 'color': 'red'},
        {'startx': '170', 'starty': '0', 'endx': '325', 'endy': '180', 'color': 'white'},
        {'startx': '325', 'starty': '0', 'endx': '480', 'endy': '180', 'color': 'yellow'},
        {'startx': '0', 'starty': '180', 'endx': '170', 'endy': '370', 'color': 'white'},
        {'startx': '0', 'starty': '370', 'endx': '170', 'endy': '480', 'color': 'yellow'},
        {'startx': '170', 'starty': '180', 'endx': '480', 'endy': '330', 'color': 'blue'},
        {'startx': '170', 'starty': '330', 'endx': '480', 'endy': '480', 'color': 'red'}
    ],

    # 4
    [
        {'startx': '0', 'starty': '0', 'endx': '140', 'endy': '100', 'color': 'blue'},
        {'startx': '140', 'starty': '0', 'endx': '480', 'endy': '100', 'color': 'white'},
        {'startx': '0', 'starty': '100', 'endx': '480', 'endy': '210', 'color': 'yellow'},
        {'startx': '0', 'starty': '210', 'endx': '330', 'endy': '480', 'color': 'white'},
        {'startx': '330', 'starty': '210', 'endx': '480', 'endy': '480', 'color': 'red'}
    ],

    # 5
    [
        {'startx': '0', 'starty': '0', 'endx': '150', 'endy': '70', 'color': 'red'},
        {'startx': '0', 'starty': '70', 'endx': '150', 'endy': '280', 'color': 'white'},
        {'startx': '0', 'starty': '280', 'endx': '150', 'endy': '480', 'color': 'yellow'},
        {'startx': '150', 'starty': '0', 'endx': '300', 'endy': '140', 'color': 'yellow'},
        {'startx': '150', 'starty': '140', 'endx': '300', 'endy': '280', 'color': 'white'},
        {'startx': '150', 'starty': '280', 'endx': '300', 'endy': '480', 'color': 'blue'},
        {'startx': '300', 'starty': '0', 'endx': '480', 'endy': '280', 'color': 'blue'},
        {'startx': '300', 'starty': '280', 'endx': '480', 'endy': '480', 'color': 'white'}
    ],

    # 6
    [
        {'startx': '0', 'starty': '0', 'endx': '70', 'endy': '70', 'color': 'yellow'},
        {'startx': '70', 'starty': '0', 'endx': '410', 'endy': '70', 'color': 'red'},
        {'startx': '410', 'starty': '0', 'endx': '480', 'endy': '70', 'color': 'yellow'},
        {'startx': '0', 'starty': '70', 'endx': '70', 'endy': '410', 'color': 'red'},
        {'startx': '70', 'starty': '70', 'endx': '240', 'endy': '240', 'color': 'blue'},
        {'startx': '240', 'starty': '70', 'endx': '410', 'endy': '240', 'color': 'blue'},
        {'startx': '70', 'starty': '240', 'endx': '240', 'endy': '410', 'color': 'blue'},
        {'startx': '240', 'starty': '240', 'endx': '410', 'endy': '410', 'color': 'blue'},
        {'startx': '410', 'starty': '70', 'endx': '480', 'endy': '410', 'color': 'red'},
        {'startx': '0', 'starty': '410', 'endx': '70', 'endy': '480', 'color': 'yellow'},
        {'startx': '70', 'starty': '410', 'endx': '410', 'endy': '480', 'color': 'red'},
        {'startx': '410', 'starty': '410', 'endx': '480', 'endy': '480', 'color': 'yellow'}

    ],

    # 7
    [
        {'startx': '0', 'starty': '0', 'endx': '140', 'endy': '480', 'color': 'red'},
        {'startx': '140', 'starty': '0', 'endx': '480', 'endy': '100', 'color': 'white'},
        {'startx': '140', 'starty': '100', 'endx': '300', 'endy': '480', 'color': 'yellow'},
        {'startx': '300', 'starty': '100', 'endx': '480', 'endy': '240', 'color': 'white'},
        {'startx': '300', 'starty': '240', 'endx': '390', 'endy': '480', 'color': 'blue'},
        {'startx': '390', 'starty': '240', 'endx': '480', 'endy': '360', 'color': 'white'},
        {'startx': '390', 'starty': '360', 'endx': '480', 'endy': '480', 'color': 'white'}
    ],

    # 8
    [
        {'startx': '0', 'starty': '0', 'endx': '120', 'endy': '100', 'color': 'red'},
        {'startx': '120', 'starty': '0', 'endx': '340', 'endy': '100', 'color': 'white'},
        {'startx': '340', 'starty': '0', 'endx': '480', 'endy': '100', 'color': 'yellow'},
        {'startx': '0', 'starty': '100', 'endx': '240', 'endy': '200', 'color': 'white'},
        {'startx': '0', 'starty': '200', 'endx': '240', 'endy': '480', 'color': 'blue'},
        {'startx': '240', 'starty': '100', 'endx': '480', 'endy': '320', 'color': 'white'},
        {'startx': '240', 'starty': '320', 'endx': '480', 'endy': '480', 'color': 'yellow'}
    ],

    # 9
    [
        {'startx': '0', 'starty': '0', 'endx': '160', 'endy': '140', 'color': 'yellow'},
        {'startx': '0', 'starty': '140', 'endx': '160', 'endy': '480', 'color': 'white'},
        {'startx': '160', 'starty': '0', 'endx': '480', 'endy': '330', 'color': 'red'},
        {'startx': '160', 'starty': '330', 'endx': '340', 'endy': '480', 'color': 'blue'},
        {'startx': '340', 'starty': '330', 'endx': '480', 'endy': '480', 'color': 'white'}
    ],

    # 10
    [
        {'startx': '0', 'starty': '0', 'endx': '370', 'endy': '100', 'color': 'white'},
        {'startx': '370', 'starty': '0', 'endx': '480', 'endy': '100', 'color': 'blue'},
        {'startx': '0', 'starty': '100', 'endx': '110', 'endy': '480', 'color': 'red'},
        {'startx': '110', 'starty': '100', 'endx': '210', 'endy': '290', 'color': 'white'},
        {'startx': '110', 'starty': '290', 'endx': '210', 'endy': '480', 'color': 'white'},
        {'startx': '210', 'starty': '100', 'endx': '480', 'endy': '290', 'color': 'white'},
        {'startx': '210', 'starty': '290', 'endx': '480', 'endy': '480', 'color': 'yellow'}
    ],

    # 11
    [
        {'startx': '0', 'starty': '0', 'endx': '160', 'endy': '160', 'color': 'red'},
        {'startx': '160', 'starty': '0', 'endx': '320', 'endy': '160', 'color': 'white'},
        {'startx': '320', 'starty': '0', 'endx': '480', 'endy': '160', 'color': 'yellow'},
        {'startx': '0', 'starty': '160', 'endx': '160', 'endy': '320', 'color': 'white'},
        {'startx': '160', 'starty': '160', 'endx': '320', 'endy': '320', 'color': 'blue'},
        {'startx': '320', 'starty': '160', 'endx': '480', 'endy': '320', 'color': 'white'},
        {'startx': '0', 'starty': '320', 'endx': '160', 'endy': '480', 'color': 'yellow'},
        {'startx': '160', 'starty': '320', 'endx': '320', 'endy': '480', 'color': 'white'},
        {'startx': '320', 'starty': '320', 'endx': '480', 'endy': '480', 'color': 'red'}
    ],

    # 12
    [
        {'startx': '0', 'starty': '0', 'endx': '480', 'endy': '230', 'color': 'blue'},
        {'startx': '0', 'starty': '230', 'endx': '240', 'endy': '480', 'color': 'yellow'},
        {'startx': '240', 'starty': '230', 'endx': '480', 'endy': '340', 'color': 'white'},
        {'startx': '240', 'starty': '340', 'endx': '360', 'endy': '480', 'color': 'red'},
        {'startx': '360', 'starty': '340', 'endx': '480', 'endy': '410', 'color': 'yellow'},
        {'startx': '360', 'starty': '410', 'endx': '420', 'endy': '480', 'color': 'white'},
        {'startx': '420', 'starty': '410', 'endx': '480', 'endy': '480', 'color': 'red'}
    ],

    # 13
    [
        {'startx': '0', 'starty': '0', 'endx': '160', 'endy': '320', 'color': 'red'},
        {'startx': '160', 'starty': '0', 'endx': '480', 'endy': '160', 'color': 'blue'},
        {'startx': '320', 'starty': '160', 'endx': '480', 'endy': '480', 'color': 'yellow'},
        {'startx': '0', 'starty': '320', 'endx': '320', 'endy': '480', 'color': 'white'},
        {'startx': '160', 'starty': '160', 'endx': '320', 'endy': '320', 'color': 'white'}
    ],

    # 14
    [
        {'startx': '0', 'starty': '0', 'endx': '290', 'endy': '180', 'color': 'white'},
        {'startx': '0', 'starty': '180', 'endx': '190', 'endy': '300', 'color': 'yellow'},
        {'startx': '190', 'starty': '180', 'endx': '290', 'endy': '300', 'color': 'blue'},
        {'startx': '0', 'starty': '300', 'endx': '290', 'endy': '480', 'color': 'white'},
        {'startx': '290', 'starty': '0', 'endx': '480', 'endy': '480', 'color': 'red'}
    ],

    # 15
    [
        {'startx': '0', 'starty': '0', 'endx': '360', 'endy': '110', 'color': 'white'},
        {'startx': '360', 'starty': '0', 'endx': '480', 'endy': '110', 'color': 'white'},
        {'startx': '0', 'starty': '110', 'endx': '360', 'endy': '160', 'color': 'white'},
        {'startx': '360', 'starty': '110', 'endx': '480', 'endy': '160', 'color': 'red'},
        {'startx': '0', 'starty': '160', 'endx': '100', 'endy': '480', 'color': 'blue'},
        {'startx': '100', 'starty': '160', 'endx': '360', 'endy': '250', 'color': 'white'},
        {'startx': '100', 'starty': '250', 'endx': '360', 'endy': '480', 'color': 'white'},
        {'startx': '360', 'starty': '160', 'endx': '480', 'endy': '360', 'color': 'white'},
        {'startx': '360', 'starty': '360', 'endx': '480', 'endy': '480', 'color': 'blue'}
    ],

    # 16
    [
        {'startx': '0', 'starty': '0', 'endx': '110', 'endy': '480', 'color': 'red'},
        {'startx': '110', 'starty': '0', 'endx': '350', 'endy': '180', 'color': 'white'},
        {'startx': '350', 'starty': '0', 'endx': '480', 'endy': '180', 'color': 'yellow'},
        {'startx': '110', 'starty': '180', 'endx': '200', 'endy': '320', 'color': 'white'},
        {'startx': '200', 'starty': '180', 'endx': '290', 'endy': '320', 'color': 'red'},
        {'startx': '110', 'starty': '320', 'endx': '290', 'endy': '480', 'color': 'white'},
        {'startx': '290', 'starty': '180', 'endx': '480', 'endy': '480', 'color': 'yellow'}
    ],

    # 17
    [
        {'startx': '0', 'starty': '0', 'endx': '360', 'endy': '150', 'color': 'yellow'},
        {'startx': '360', 'starty': '0', 'endx': '480', 'endy': '150', 'color': 'blue'},
        {'startx': '0', 'starty': '150', 'endx': '160', 'endy': '480', 'color': 'blue'},
        {'startx': '160', 'starty': '150', 'endx': '480', 'endy': '270', 'color': 'white'},
        {'startx': '160', 'starty': '270', 'endx': '320', 'endy': '480', 'color': 'white'},
        {'startx': '320', 'starty': '270', 'endx': '480', 'endy': '480', 'color': 'red'},
    ],

    # 18
    [
        {'startx': '0', 'starty': '0', 'endx': '60', 'endy': '60', 'color': 'white'},
        {'startx': '60', 'starty': '0', 'endx': '120', 'endy': '60', 'color': 'white'},
        {'startx': '120', 'starty': '0', 'endx': '360', 'endy': '60', 'color': 'white'},
        {'startx': '360', 'starty': '0', 'endx': '420', 'endy': '60', 'color': 'white'},
        {'startx': '480', 'starty': '0', 'endx': '480', 'endy': '60', 'color': 'white'},
        {'startx': '0', 'starty': '60', 'endx': '60', 'endy': '120', 'color': 'white'},
        {'startx': '60', 'starty': '60', 'endx': '120', 'endy': '120', 'color': 'white'},
        {'startx': '120', 'starty': '60', 'endx': '360', 'endy': '120', 'color': 'white'},
        {'startx': '360', 'starty': '60', 'endx': '420', 'endy': '120', 'color': 'blue'},
        {'startx': '480', 'starty': '60', 'endx': '480', 'endy': '120', 'color': 'white'},
        {'startx': '0', 'starty': '120', 'endx': '60', 'endy': '360', 'color': 'yellow'},
        {'startx': '60', 'starty': '120', 'endx': '120', 'endy': '360', 'color': 'white'},
        {'startx': '120', 'starty': '120', 'endx': '360', 'endy': '360', 'color': 'white'},
        {'startx': '360', 'starty': '120', 'endx': '420', 'endy': '360', 'color': 'white'},
        {'startx': '420', 'starty': '120', 'endx': '480', 'endy': '360', 'color': 'white'},
        {'startx': '0', 'starty': '360', 'endx': '60', 'endy': '420', 'color': 'white'},
        {'startx': '60', 'starty': '360', 'endx': '120', 'endy': '420', 'color': 'white'},
        {'startx': '120', 'starty': '360', 'endx': '360', 'endy': '420', 'color': 'white'},
        {'startx': '360', 'starty': '360', 'endx': '420', 'endy': '420', 'color': 'white'},
        {'startx': '420', 'starty': '360', 'endx': '480', 'endy': '420', 'color': 'white'},
        {'startx': '0', 'starty': '420', 'endx': '60', 'endy': '480', 'color': 'white'},
        {'startx': '60', 'starty': '420', 'endx': '120', 'endy': '480', 'color': 'white'},
        {'startx': '120', 'starty': '420', 'endx': '360', 'endy': '480', 'color': 'white'},
        {'startx': '360', 'starty': '420', 'endx': '420', 'endy': '480', 'color': 'white'},
        {'startx': '420', 'starty': '420', 'endx': '480', 'endy': '480', 'color': 'white'}
    ],

    # 19
    [
        {'startx': '0', 'starty': '0', 'endx': '140', 'endy': '480', 'color': 'red'},
        {'startx': '140', 'starty': '0', 'endx': '480', 'endy': '120', 'color': 'white'},
        {'startx': '140', 'starty': '120', 'endx': '390', 'endy': '300', 'color': 'blue'},
        {'startx': '390', 'starty': '120', 'endx': '480', 'endy': '300', 'color': 'white'},
        {'startx': '140', 'starty': '300', 'endx': '270', 'endy': '480', 'color': 'white'},
        {'startx': '270', 'starty': '300', 'endx': '480', 'endy': '480', 'color': 'yellow'}
    ],

    # 20
    [
        {'startx': '0', 'starty': '0', 'endx': '60', 'endy': '130', 'color': 'white'},
        {'startx': '60', 'starty': '0', 'endx': '250', 'endy': '130', 'color': 'yellow'},
        {'startx': '250', 'starty': '0', 'endx': '370', 'endy': '130', 'color': 'white'},
        {'startx': '370', 'starty': '0', 'endx': '480', 'endy': '130', 'color': 'blue'},
        {'startx': '0', 'starty': '130', 'endx': '60', 'endy': '480', 'color': 'yellow'},
        {'startx': '60', 'starty': '130', 'endx': '250', 'endy': '310', 'color': 'red'},
        {'startx': '250', 'starty': '130', 'endx': '480', 'endy': '310', 'color': 'white'},
        {'startx': '60', 'starty': '310', 'endx': '250', 'endy': '480', 'color': 'white'},
        {'startx': '250', 'starty': '310', 'endx': '480', 'endy': '480', 'color': 'blue'}
    ],

    # 21
    [
        {'startx': '0', 'starty': '0', 'endx': '80', 'endy': '70', 'color': 'red'},
        {'startx': '80', 'starty': '0', 'endx': '130', 'endy': '70', 'color': 'white'},
        {'startx': '130', 'starty': '0', 'endx': '480', 'endy': '70', 'color': 'white'},
        {'startx': '0', 'starty': '70', 'endx': '80', 'endy': '480', 'color': 'white'},
        {'startx': '80', 'starty': '70', 'endx': '130', 'endy': '130', 'color': 'white'},
        {'startx': '130', 'starty': '70', 'endx': '480', 'endy': '130', 'color': 'red'},
        {'startx': '80', 'starty': '130', 'endx': '130', 'endy': '480', 'color': 'white'},
        {'startx': '130', 'starty': '130', 'endx': '200', 'endy': '220', 'color': 'white'},
        {'startx': '200', 'starty': '130', 'endx': '480', 'endy': '220', 'color': 'white'},
        {'startx': '130', 'starty': '220', 'endx': '200', 'endy': '480', 'color': 'yellow'},
        {'startx': '200', 'starty': '220', 'endx': '480', 'endy': '480', 'color': 'white'}
    ],

    # 22
    [
        {'startx': '0', 'starty': '0', 'endx': '70', 'endy': '60', 'color': 'white'},
        {'startx': '70', 'starty': '0', 'endx': '410', 'endy': '60', 'color': 'white'},
        {'startx': '410', 'starty': '0', 'endx': '480', 'endy': '60', 'color': 'blue'},
        {'startx': '0', 'starty': '60', 'endx': '70', 'endy': '350', 'color': 'white'},
        {'startx': '0', 'starty': '350', 'endx': '70', 'endy': '480', 'color': 'white'},
        {'startx': '70', 'starty': '60', 'endx': '410', 'endy': '150', 'color': 'white'},
        {'startx': '70', 'starty': '150', 'endx': '300', 'endy': '480', 'color': 'yellow'},
        {'startx': '300', 'starty': '150', 'endx': '410', 'endy': '480', 'color': 'white'},
        {'startx': '410', 'starty': '60', 'endx': '480', 'endy': '480', 'color': 'white'}
    ],

    # 23
    [
        {'startx': '0', 'starty': '0', 'endx': '120', 'endy': '80', 'color': 'blue'},
        {'startx': '120', 'starty': '0', 'endx': '150', 'endy': '80', 'color': 'yellow'},
        {'startx': '150', 'starty': '0', 'endx': '480', 'endy': '80', 'color': 'blue'},
        {'startx': '0', 'starty': '80', 'endx': '120', 'endy': '120', 'color': 'yellow'},
        {'startx': '120', 'starty': '80', 'endx': '150', 'endy': '120', 'color': 'white'},
        {'startx': '150', 'starty': '80', 'endx': '480', 'endy': '120', 'color': 'yellow'},
        {'startx': '0', 'starty': '120', 'endx': '120', 'endy': '480', 'color': 'blue'},
        {'startx': '120', 'starty': '120', 'endx': '150', 'endy': '480', 'color': 'yellow'},
        {'startx': '150', 'starty': '120', 'endx': '480', 'endy': '480', 'color': 'blue'}
    ],

    # 24
    [
        {'startx': '0', 'starty': '0', 'endx': '480', 'endy': '90', 'color': 'white'},
        {'startx': '0', 'starty': '90', 'endx': '96', 'endy': '390', 'color': 'yellow'},
        {'startx': '96', 'starty': '90', 'endx': '192', 'endy': '390', 'color': 'white'},
        {'startx': '192', 'starty': '90', 'endx': '288', 'endy': '390', 'color': 'white'},
        {'startx': '288', 'starty': '90', 'endx': '384', 'endy': '390', 'color': 'yellow'},
        {'startx': '384', 'starty': '90', 'endx': '480', 'endy': '390', 'color': 'white'},
        {'startx': '0', 'starty': '390', 'endx': '480', 'endy': '480', 'color': 'blue'}
    ],

    # 25
    [
        {'startx': '0', 'starty': '0', 'endx': '160', 'endy': '480', 'color': 'red'},
        {'startx': '160', 'starty': '0', 'endx': '320', 'endy': '480', 'color': 'white'},
        {'startx': '320', 'starty': '0', 'endx': '480', 'endy': '480', 'color': 'blue'}
    ],

    # 26
    [
        {'startx': '0', 'starty': '0', 'endx': '100', 'endy': '380', 'color': 'blue'},
        {'startx': '100', 'starty': '0', 'endx': '480', 'endy': '380', 'color': 'yellow'},
        {'startx': '0', 'starty': '380', 'endx': '100', 'endy': '480', 'color': 'white'},
        {'startx': '100', 'starty': '380', 'endx': '480', 'endy': '480', 'color': 'red'}
    ],

    # 27
    [
        {'startx': '0', 'starty': '0', 'endx': '360', 'endy': '50', 'color': 'yellow'},
        {'startx': '0', 'starty': '50', 'endx': '360', 'endy': '100', 'color': 'white'},
        {'startx': '0', 'starty': '100', 'endx': '180', 'endy': '480', 'color': 'white'},
        {'startx': '180', 'starty': '100', 'endx': '360', 'endy': '480', 'color': 'red'},
        {'startx': '360', 'starty': '0', 'endx': '480', 'endy': '70', 'color': 'white'},
        {'startx': '360', 'starty': '70', 'endx': '480', 'endy': '280', 'color': 'white'},
        {'startx': '360', 'starty': '280', 'endx': '480', 'endy': '480', 'color': 'yellow'}
    ]
]

multiple_ui    =[0, 0, 1, 1, 2, 2, 3, 3];
multiple_single=[0, 1, 0, 1, 0 ,1, 0, 1];

@csrf_exempt
def render_question_page(request, questionMap):
    return render(request, question_codename + '/index.html',
                  questionMap);

@csrf_exempt
def start_multiple_choices(request):
    uid=request.GET.get('uid');
    if uid==None:
        return HttpResponseNotFound('<h1>Invalid Request</h1>');
    iteration_num=request.GET.get('iteration');
    if iteration_num==None:
        return HttpResponseNotFound('<h1>Invalid Request</h1>');
    # Get ui index.
    iteration_num=int(iteration_num);
    # Check iteration.
    if iteration_num>7:
        return HttpResponseNotFound('<h1>Invalid Request</h1>');

    # Find last iteration gene information.
    gene_title=uid+"|iteration"+str(iteration_num)+"-gene";
    searchList=ExpResult.objects.filter(title=gene_title);
    if(len(searchList)==0):
        return HttpResponseNotFound('<h1>Invalid Request - No Gene Found</h1>');
    gene_title=searchList[0].result;
    # Load the gene as json.
    iterationImageGene=json.loads(gene_title);

    singleIndex=request.GET.get('single');
    if singleIndex==None:
        singleIndex=multiple_single[iteration_num];
    else:
        singleIndex=int(singleIndex);
        if singleIndex>1:
            singleIndex=0;
    uiIndex=request.GET.get('ui');
    if uiIndex==None:
        uiIndex=multiple_ui[iteration_num];
    else:
        uiIndex=int(uiIndex);
        if uiIndex>3:
            uiIndex=0;

    iteration_image_list=[];
    for i in range(0, 27):
        imagePath="static/hash_images/"+uid+"-i"+str(iteration_num)+"-"+str(i)+".png";
        iteration_image_list.append(imagePath);
    return render(request, multiple_choice_codename + '/index.html',
                  {'testList':iteration_image_list,
                   'testTitle':"'Mondrian Painting #'",
                   'testHintText':"'Choose the images you like'",
                   'testScoreHintText':"'Score the chosen images'",
                   'testDriveHintText':"'Use A(left), W(mid), D(right) to select the group contains the most image you like'",
                   'testDriveConfirmText':"'Hit the same key again to confirm, or S(back) to cancel'",
                   'testSingleIndex':singleIndex,
                   'testUIIndex':uiIndex,
                   'testIteration':iteration_num,
                   'uid':uid,
                   'imageGene':iterationImageGene});

@csrf_exempt
def start_initial_test(request):
    # Check request.
    uid=request.COOKIES.get('uid', 'none');
    if(uid=='none'):
        return HttpResponseNotFound('<h1>Invalid Request</h1>');
    return render(request, single_choice_codename + '/index.html',
                  {'testImage': ['static/images/1.png',
                                #  'static/images/2.png',
                                #  'static/images/3.png',
                                #  'static/images/4.png',
                                #  'static/images/5.png',
                                #  'static/images/6.png',
                                #  'static/images/7.png',
                                #  'static/images/8.png',
                                #  'static/images/9.png',
                                #  'static/images/10.png',
                                #  'static/images/11.png',
                                #  'static/images/12.png',
                                #  'static/images/13.png',
                                #  'static/images/14.png',
                                #  'static/images/15.png',
                                #  'static/images/16.png',
                                #  'static/images/17.png',
                                #  'static/images/18.png',
                                #  'static/images/19.png',
                                #  'static/images/20.png',
                                #  'static/images/21.png',
                                #  'static/images/22.png',
                                #  'static/images/23.png',
                                #  'static/images/24.png',
                                #  'static/images/25.png',
                                #  'static/images/26.png',
                                 'static/images/27.png'],
                    'testList': [0,
                                #  0,0,0,0,
                                #  1,1,1,1,1,
                                #  2,2,2,2,2,
                                #  3,3,3,3,3,
                                #  4,4,4,4,4,4,
                                 4],
                    'testHintText': ['Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Do you like this image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                    #  'Please indicate how much you like the image?',
                                     'Please indicate how much you like the image?'],
                    'testLabel': [[],
                                #   [],
                                #   [],
                                #   [],
                                #   [],
                                #   [],
                                #   [],
                                #   [],
                                #   [],
                                #   [],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                #   ['Dislike', 'So-so', 'Like'],
                                  ['Dislike', 'So-so', 'Like']],
                    'testRadioMaximum': 7,
                    'testInstructionTitle': '"Part 2 - Single Image Response Experiment"',
                    'testInstructionText': '"In the following experiment, you have to rate 20 Mondrian\'s Neo-Plasticism style paintings. You have to score each image as how much you like it, but not how much artistic value it has.</p><p>In the experiment, you will use buttons, stars and sliders to score the paintings.</p><p>Click \'start\' when you are ready."',
                    'imageGene' : imageList});

def add_question(questionMap, questionType, questionText, questionExplain, questionSetting):
    questionMap['questionTypes'].append(questionType.value);
    questionMap['questionTexts'].append(questionText);
    questionMap['questionExplains'].append(questionExplain);
    questionMap['questionSettings'].append(questionSetting);

@csrf_exempt
def start_question(request):
    questionMap={'questionTypes': [],
                 'questionTexts': [],
                 'questionExplains': [],
                 'questionSettings': []};
    add_question(questionMap,
                 Question_Type.Text,
                 "Please input your ANU ID",
                 "Your ANU ID is assigned when you become a student or staff member at the University, and is in the format of u1234567",
                 {"defaultText": "Your ANU ID, e.g.: u1234567"});

    add_question(questionMap,
                 Question_Type.Combo,
                 "What is your gender?",
                 "Please select your gender in the following dropdown box",
                 {"defaultText":"Gender",
                  "values": [["Male", "0"],
                             ["Female", "1"]]});

    add_question(questionMap,
                 Question_Type.Slider,
                 "What is your age?",
                 "Please select your age in the slider",
                 {"min" : 16,
                  "max" : 100,
                  "label" : "My age is"});

    add_question(questionMap,
                 Question_Type.SearchCombo,
                 "Which program are you in now?",
                 "Please select the program you are studying now. If none of them matches you, please select 'Other'.",
                 {"defaultText":"Your ANU program",
                  "values": [["ANU Express", "0"],
                             ["ANU Preparatory Program", "1"],
                             ["ANU Summer Research Scholarship Program", "2"],
                             ["Associate Degree", "3"],
                             ["Bachelor of Accounting", "4"],
                             ["Bachelor of Accounting (Honours)", "5"],
                             ["Bachelor of Actuarial Studies", "6"],
                             ["Bachelor of Actuarial Studies (Honours)", "7"],
                             ["Bachelor of Advanced Computing (Honours)", "8"],
                             ["Bachelor of Advanced Computing (Research and Development) (Honours)", "9"],
                             ["Bachelor of Archaeological Practice", "10"],
                             ["Bachelor of Archaeological Practice (Honours)", "11"],
                             ["Bachelor of Art History and Curatorship", "12"],
                             ["Bachelor of Art History and Curatorship (Honours)", "13"],
                             ["Bachelor of Arts", "14"],
                             ["Bachelor of Arts (Honours)", "15"],
                             ["Bachelor of Arts (Honours)", "16"],
                             ["Bachelor of Asian Studies", "17"],
                             ["Bachelor of Asian Studies (Honours)", "18"],
                             ["Bachelor of Asia-Pacific Studies (Year in Asia)", "19"],
                             ["Bachelor of Biotechnology", "20"],
                             ["Bachelor of Biotechnology (Honours)", "21"],
                             ["Bachelor of Business Administration", "22"],
                             ["Bachelor of Business Administration (Honours)", "23"],
                             ["Bachelor of Classical Studies", "24"],
                             ["Bachelor of Classical Studies (Honours)", "25"],
                             ["Bachelor of Commerce", "26"],
                             ["Bachelor of Commerce (Honours)", "27"],
                             ["Bachelor of Criminology", "28"],
                             ["Bachelor of Criminology (Honours)", "29"],
                             ["Bachelor of Design", "30"],
                             ["Bachelor of Design Arts (Honours)", "31"],
                             ["Bachelor of Development Studies", "32"],
                             ["Bachelor of Development Studies (Honours)", "33"],
                             ["Bachelor of Economics", "34"],
                             ["Bachelor of Economics (Honours)", "35"],
                             ["Bachelor of Engineering (Honours)", "36"],
                             ["Bachelor of Engineering (Research and Development) (Honours)", "37"],
                             ["Bachelor of Environment and Sustainability", "38"],
                             ["Bachelor of Environment and Sustainability (Honours)", "39"],
                             ["Bachelor of Environment and Sustainability Advanced (Honours)", "40"],
                             ["Bachelor of Environmental Studies", "41"],
                             ["Bachelor of Environmental Studies (Honours)", "42"],
                             ["Bachelor of European Studies", "43"],
                             ["Bachelor of European Studies (Honours)", "44"],
                             ["Bachelor of Finance", "45"],
                             ["Bachelor of Finance (Honours)", "46"],
                             ["Bachelor of Finance, Economics and Statistics (Honours)", "47"],
                             ["Bachelor of Genetics", "48"],
                             ["Bachelor of Genetics (Honours)", "49"],
                             ["Bachelor of Information Technology", "50"],
                             ["Bachelor of Information Technology (Honours)", "51"],
                             ["Bachelor of International Business", "52"],
                             ["Bachelor of International Business (Honours)", "53"],
                             ["Bachelor of International Relations", "54"],
                             ["Bachelor of International Relations (Honours)", "55"],
                             ["Bachelor of International Security Studies", "56"],
                             ["Bachelor of International Security Studies (Honours)", "57"],
                             ["Bachelor of Languages", "58"],
                             ["Bachelor of Languages (Honours)", "59"],
                             ["Bachelor of Latin American Studies", "60"],
                             ["Bachelor of Latin American Studies (Honours)", "61"],
                             ["Bachelor of Laws (Honours)", "62"],
                             ["Bachelor of Mathematical Sciences", "63"],
                             ["Bachelor of Medical Science", "64"],
                             ["Bachelor of Medical Science (Honours)", "65"],
                             ["Bachelor of Medical Science (Honours)", "66"],
                             ["Bachelor of Middle Eastern and Central Asian Studies", "67"],
                             ["Bachelor of Middle Eastern and Central Asian Studies (Honours)", "68"],
                             ["Bachelor of Music", "69"],
                             ["Bachelor of Music (Honours)", "70"],
                             ["Bachelor of Pacific Studies", "71"],
                             ["Bachelor of Philosophy (Honours) - Arts and Social Science", "72"],
                             ["Bachelor of Philosophy (Honours) - Asia and the Pacific", "73"],
                             ["Bachelor of Philosophy (Honours) - Science", "74"],
                             ["Bachelor of Philosophy (Honours) / Bachelor of Arts (Honours)", "75"],
                             ["Bachelor of Philosophy (Honours) / Bachelor of Science (Honours) - ANU as home institution", "76"],
                             ["Bachelor of Philosophy (Honours) / Bachelor of Science (Honours) - NUS as home institution", "77"],
                             ["Bachelor of Policy Studies", "78"],
                             ["Bachelor of Policy Studies (Honours)", "79"],
                             ["Bachelor of Political Science", "80"],
                             ["Bachelor of Political Science (Honours)", "81"],
                             ["Bachelor of Politics, Philosophy and Economics", "82"],
                             ["Bachelor of Politics, Philosophy and Economics (Honours)", "83"],
                             ["Bachelor of Psychology (Honours)", "84"],
                             ["Bachelor of Science", "85"],
                             ["Bachelor of Science (Advanced) (Honours)", "86"],
                             ["Bachelor of Science (Honours)", "87"],
                             ["Bachelor of Science (Psychology)", "88"],
                             ["Bachelor of Science (Psychology) (Honours)", "89"],
                             ["Bachelor of Social Sciences (Honours in Actuarial Studies and Economics)", "90"],
                             ["Bachelor of Software Engineering (Honours)", "91"],
                             ["Bachelor of Statistics", "92"],
                             ["Bachelor of Statistics (Honours)", "93"],
                             ["Bachelor of Studies", "94"],
                             ["Bachelor of Visual Arts", "95"],
                             ["Bachelor of Visual Arts (Honours)", "96"],
                             ["Cross Institutional Research", "97"],
                             ["Diploma of Advanced Studies", "98"],
                             ["Diploma of Computing", "99"],
                             ["Diploma of Languages", "100"],
                             ["Diploma of Liberal Studies", "101"],
                             ["Diploma of Music", "102"],
                             ["Doctor of Juridical Science (SJD), ANU College of Law", "103"],
                             ["Doctor of Laws", "104"],
                             ["Doctor of Letters", "105"],
                             ["Doctor of Medicine", "106"],
                             ["Doctor of Medicine and Surgery", "107"],
                             ["Doctor of Philosophy", "108"],
                             ["Doctor of Philosophy (Clinical Psychology)", "109"],
                             ["Doctor of Philosophy, ANU College of Business and Economics", "110"],
                             ["Doctor of Philosophy, ANU College of Engineering and Computer Science", "111"],
                             ["Doctor of Philosophy, ANU College of Law", "112"],
                             ["Doctor of Philosophy, ANU Colleges of Science (Joint Degree ANU-NUS)", "113"],
                             ["Doctor of Philosophy, ANU/NTNU", "114"],
                             ["Doctor of Philosophy, Australian Centre on China in the World", "115"],
                             ["Doctor of Philosophy, Crawford School of Public Policy", "116"],
                             ["Doctor of Philosophy, Culture History and Languages", "117"],
                             ["Doctor of Philosophy, Diplomacy", "118"],
                             ["Doctor of Philosophy, Fenner School of Environment and Society", "119"],
                             ["Doctor of Philosophy, International, Political and Strategic Studies", "120"],
                             ["Doctor of Philosophy, John Curtin School of Medical Research", "121"],
                             ["Doctor of Philosophy, Mathematical Sciences Institute", "122"],
                             ["Doctor of Philosophy, Medical School", "123"],
                             ["Doctor of Philosophy, National Centre for Indigenous Studies", "124"],
                             ["Doctor of Philosophy, National Security College", "125"],
                             ["Doctor of Philosophy, Psychology", "126"],
                             ["Doctor of Philosophy, Regulation, Justice and Diplomacy", "127"],
                             ["Doctor of Philosophy, Research School of Astronomy and Astrophysics", "128"],
                             ["Doctor of Philosophy, Research School of Biology", "129"],
                             ["Doctor of Philosophy, Research School of Chemistry", "130"],
                             ["Doctor of Philosophy, Research School of Earth Sciences", "131"],
                             ["Doctor of Philosophy, Research School of Humanities and the Arts", "132"],
                             ["Doctor of Philosophy, Research School of Physics and Engineering", "133"],
                             ["Doctor of Philosophy, Research School of Population Health", "134"],
                             ["Doctor of Philosophy, Research School of Social Sciences", "135"],
                             ["Doctor of Philosophy, Science", "136"],
                             ["Doctor of Psychology (Clinical)", "137"],
                             ["Doctor of Science", "138"],
                             ["Executive Master of Public Administration", "139"],
                             ["Flexible Double Degree", "140"],
                             ["Flexible Double Degree - Arts, Social Sciences, Business, Science", "141"],
                             ["Flexible Double Degree – Law (Honours)", "142"],
                             ["Flexible Double Masters", "143"],
                             ["Global Summer Program (Postgraduate)", "144"],
                             ["Global Summer Program (Undergraduate)", "145"],
                             ["Graduate Bridging Program (Crawford School of Public Policy)", "146"],
                             ["Graduate Certificate in Australian Migration Law and Practice", "147"],
                             ["Graduate Certificate of Accounting", "148"],
                             ["Graduate Certificate of Applied Data Analytics", "149"],
                             ["Graduate Certificate of Applied Epidemiology", "150"],
                             ["Graduate Certificate of Arts", "151"],
                             ["Graduate Certificate of Business Information Management", "152"],
                             ["Graduate Certificate of Economics", "153"],
                             ["Graduate Certificate of Environment", "154"],
                             ["Graduate Certificate of Finance and Actuarial Statistics", "155"],
                             ["Graduate Certificate of Law", "156"],
                             ["Graduate Certificate of Management", "157"],
                             ["Graduate Certificate of Military and Defence Studies", "158"],
                             ["Graduate Certificate of Military Law", "159"],
                             ["Graduate Certificate of Public Health", "160"],
                             ["Graduate Certificate of Public Policy", "161"],
                             ["Graduate Certificate of Science", "162"],
                             ["Graduate Certificate of Studies", "163"],
                             ["Graduate Certificate of Studies - Online", "164"],
                             ["Graduate Certificate of Teaching Asia", "165"],
                             ["Graduate Diploma of Accounting", "166"],
                             ["Graduate Diploma of Applied Data Analytics", "167"],
                             ["Graduate Diploma of Business Information Systems", "168"],
                             ["Graduate Diploma of Computing", "169"],
                             ["Graduate Diploma of Economics", "170"],
                             ["Graduate Diploma of Environment", "171"],
                             ["Graduate Diploma of Finance and Actuarial Statistics", "172"],
                             ["Graduate Diploma of International Affairs", "173"],
                             ["Graduate Diploma of Legal Practice", "174"],
                             ["Graduate Diploma of Military and Defence Studies", "175"],
                             ["Graduate Diploma of Military Law", "176"],
                             ["Graduate Diploma of Public Health", "177"],
                             ["Graduate Diploma of Public Policy", "178"],
                             ["Graduate Diploma of Science", "179"],
                             ["Graduate Diploma of Studies", "180"],
                             ["Graduate Exchange Program", "181"],
                             ["Graduate Exchange Program", "182"],
                             ["Graduate Non-Award", "183"],
                             ["Graduate Non-Award - Applied Data Analytics", "184"],
                             ["Graduate Non-Award (ANU College of Arts and Social Sciences)", "185"],
                             ["Graduate Non-Award (ANU College of Business & Economics)", "186"],
                             ["Graduate Non-Award (ANU College of Law)", "187"],
                             ["Graduate Non-Award (ANU Colleges of Science)", "188"],
                             ["Graduate Non-Award (College of Engineering and Computer Science)", "189"],
                             ["Graduate Non-Award (Examination)", "190"],
                             ["Graduate Non-Award (Legal Workshop)", "191"],
                             ["Graduate Non-Award (Research)", "192"],
                             ["Graduate Non-Award (School of Culture, History and Language)", "193"],
                             ["Graduate Non-Award Cross Institutional (ANU College of Medicine Biology and Environment)", "194"],
                             ["Graduate Non-Award Cross-Institutional ", "195"],
                             ["Graduate Non-Award Cross-Institutional (ANU College of Arts and Social Sciences)", "196"],
                             ["Graduate Non-Award Cross-Institutional (ANU College of Asia and the Pacific)", "197"],
                             ["Graduate Non-Award Cross-Institutional (ANU College of Business and Economics)", "198"],
                             ["Graduate Non-Award Cross-Institutional (ANU College of Engineering and Computer Science)", "199"],
                             ["Graduate Non-Award Cross-Institutional (ANU College of Law)", "200"],
                             ["Graduate Non-Award Cross-Institutional (ANU College of Law)", "201"],
                             ["Graduate Non-Award Cross-Institutional (ANU Colleges of Science)", "202"],
                             ["Graduate Non-Award Examination", "203"],
                             ["Graduate Non-Award, National Security College", "204"],
                             ["Graduate Study Abroad Program", "205"],
                             ["Joint Degree Program National University Singapore -The Australian National University", "206"],
                             ["Joint Doctor of Philosophy, The Australian National University - National University Singapore", "207"],
                             ["Joint Postgraduate Program National University Singapore - The Australian National University (Asia-Pacific       Studies)", "208"],
                             ["Juris Doctor", "209"],
                             ["Juris Doctor - online", "210"],
                             ["Juris Doctor (Honours)", "211"],
                             ["Master of Accounting", "212"],
                             ["Master of Actuarial Practice", "213"],
                             ["Master of Actuarial Studies", "214"],
                             ["Master of Anthropology", "215"],
                             ["Master of Anthropology (Advanced)", "216"],
                             ["Master of Applied Anthropology and Participatory Development", "217"],
                             ["Master of Applied Anthropology and Participatory Development - Online", "218"],
                             ["Master of Applied Anthropology and Participatory Development (Advanced)", "219"],
                             ["Master of Applied Anthropology and Participatory Development (Advanced) - Online", "220"],
                             ["Master of Applied Data Analytics", "221"],
                             ["Master of Applied Economics", "222"],
                             ["Master of Applied Finance", "223"],
                             ["Master of Archaeological Science", "224"],
                             ["Master of Archaeological Science (Advanced)", "225"],
                             ["Master of Art History and Curatorial Studies", "226"],
                             ["Master of Art History and Curatorial Studies (Advanced)", "227"],
                             ["Master of Arts (Advanced)", "228"],
                             ["Master of Asia-Pacific Studies", "229"],
                             ["Master of Astronomy and Astrophysics (Advanced)", "230"],
                             ["Master of Biological Anthropology", "231"],
                             ["Master of Biological Anthropology (Advanced)", "232"],
                             ["Master of Biological Sciences", "233"],
                             ["Master of Biological Sciences (Advanced)", "234"],
                             ["Master of Biotechnology", "235"],
                             ["Master of Biotechnology (Advanced)", "236"],
                             ["Master of Business Administration", "237"],
                             ["Master of Business Administration (Advanced)", "238"],
                             ["Master of Business Information Systems", "239"],
                             ["Master of Classical Studies", "240"],
                             ["Master of Classical Studies (Advanced)", "241"],
                             ["Master of Climate Change", "242"],
                             ["Master of Clinical Psychology", "243"],
                             ["Master of Commerce", "244"],
                             ["Master of Computing", "245"],
                             ["Master of Computing (Advanced)", "246"],
                             ["Master of Culture Health and Medicine (Advanced)", "247"],
                             ["Master of Culture, Health and Medicine", "248"],
                             ["Master of Demography", "249"],
                             ["Master of Design", "250"],
                             ["Master of Design (Advanced)", "251"],
                             ["Master of Digital Arts", "252"],
                             ["Master of Digital Arts (Advanced)", "253"],
                             ["Master of Digital Humanities and Public Culture", "254"],
                             ["Master of Digital Humanities and Public Culture (Advanced)", "255"],
                             ["Master of Diplomacy", "256"],
                             ["Master of Diplomacy (Advanced)", "257"],
                             ["Master of Earth Sciences (Advanced)", "258"],
                             ["Master of Economic Policy", "259"],
                             ["Master of Economics", "260"],
                             ["Master of Energy Change", "261"],
                             ["Master of Energy Change (Advanced)", "262"],
                             ["Master of Engineering in Digital Systems and Telecommunications", "263"],
                             ["Master of Engineering in Mechatronics", "264"],
                             ["Master of Engineering in Photonics", "265"],
                             ["Master of Engineering in Renewable Energy", "266"],
                             ["Master of Entrepreneurship and Innovation", "267"],
                             ["Master of Entrepreneurship and Innovation (Advanced)", "268"],
                             ["Master of Environment", "269"],
                             ["Master of Environment (Advanced)", "270"],
                             ["Master of Environmental and Resource Economics", "271"],
                             ["Master of Environmental Management and Development", "272"],
                             ["Master of Environmental Management and Development - Online", "273"],
                             ["Master of Environmental Science", "274"],
                             ["Master of Environmental Science (Advanced)", "275"],
                             ["Master of Finance", "276"],
                             ["Master of Financial Economics", "277"],
                             ["Master of Financial Management", "278"],
                             ["Master of Forestry", "279"],
                             ["Master of Forestry (Advanced)", "280"],
                             ["Master of General and Applied Linguistics", "281"],
                             ["Master of General and Applied Linguistics (Advanced)", "282"],
                             ["Master of Globalisation", "283"],
                             ["Master of Globalisation (Advanced)", "284"],
                             ["Master of History", "285"],
                             ["Master of History (Advanced)", "286"],
                             ["Master of Innovation and Professional Practice", "287"],
                             ["Master of International Affairs", "288"],
                             ["Master of International and Development Economics", "289"],
                             ["Master of International Management", "290"],
                             ["Master of International Management (Advanced)", "291"],
                             ["Master of International Relations", "292"],
                             ["Master of International Relations (Advanced)", "293"],
                             ["Master of Islam in the Modern World", "294"],
                             ["Master of Islam in the Modern World (Advanced)", "295"],
                             ["Master of Laws", "296"],
                             ["Master of Laws in Environmental Law", "297"],
                             ["Master of Laws in Government and Regulation", "298"],
                             ["Master of Laws in International Law", "299"],
                             ["Master of Laws in International Security Law", "300"],
                             ["Master of Laws in Law, Governance and Development", "301"],
                             ["Master of Laws in Migration Law", "302"],
                             ["Master of Leadership", "303"],
                             ["Master of Leadership (Advanced)", "304"],
                             ["Master of Legal Practice", "305"],
                             ["Master of Management", "306"],
                             ["Master of Management (Advanced)", "307"],
                             ["Master of Marketing Management", "308"],
                             ["Master of Marketing Management (Advanced)", "309"],
                             ["Master of Mathematical Sciences (Advanced)", "310"],
                             ["Master of Middle Eastern and Central Asian Studies", "311"],
                             ["Master of Middle Eastern and Central Asian Studies (Advanced)", "312"],
                             ["Master of Military and Defence Studies", "313"],
                             ["Master of Military and Defence Studies (Advanced)", "314"],
                             ["Master of Military Law", "315"],
                             ["Master of Museum and Heritage Studies", "316"],
                             ["Master of Museum and Heritage Studies (Advanced)", "317"],
                             ["Master of Music", "318"],
                             ["Master of Music (Advanced)", "319"],
                             ["Master of National Security Policy", "320"],
                             ["Master of National Security Policy (Advanced)", "321"],
                             ["Master of Neuroscience", "322"],
                             ["Master of Neuroscience (Advanced)", "323"],
                             ["Master of Nuclear Science", "324"],
                             ["Master of Philosophy", "325"],
                             ["Master of Philosophy (MPhil), ANU College of Law", "326"],
                             ["Master of Philosophy in Applied Epidemiology", "327"],
                             ["Master of Philosophy, ANU College of Business and Economics", "328"],
                             ["Master of Philosophy, ANU College of Engineering and Computer Science", "329"],
                             ["Master of Philosophy, ANU Colleges of Science", "330"],
                             ["Master of Philosophy, ANU Medical School", "331"],
                             ["Master of Philosophy, Crawford School of Public Policy", "332"],
                             ["Master of Philosophy, Culture, History and Languages", "333"],
                             ["Master of Philosophy, Fenner School of Environment and Society", "334"],
                             ["Master of Philosophy, John Curtin School of Medical Research", "335"],
                             ["Master of Philosophy, Mathematical Sciences Institute", "336"],
                             ["Master of Philosophy, National Centre for Indigenous Studies", "337"],
                             ["Master of Philosophy, National Security College", "338"],
                             ["Master of Philosophy, Psychology", "339"],
                             ["Master of Philosophy, Regulation, Justice and Diplomacy", "340"],
                             ["Master of Philosophy, Research School of Astronomy and Astrophysics", "341"],
                             ["Master of Philosophy, Research School of Biology", "342"],
                             ["Master of Philosophy, Research School of Chemistry", "343"],
                             ["Master of Philosophy, Research School of Earth Sciences", "344"],
                             ["Master of Philosophy, Research School of Humanities and the Arts", "345"],
                             ["Master of Philosophy, Research School of Physics and Engineering", "346"],
                             ["Master of Philosophy, Research School of Population Health", "347"],
                             ["Master of Philosophy, Research School of Social Sciences", "348"],
                             ["Master of Philosophy, School of International, Political and Strategic Studies", "349"],
                             ["Master of Professional Accounting", "350"],
                             ["Master of Project Management", "351"],
                             ["Master of Public Administration", "352"],
                             ["Master of Public Health", "353"],
                             ["Master of Public Health (Advanced)", "354"],
                             ["Master of Public Policy", "355"],
                             ["Master of Public Policy in Development Policy", "356"],
                             ["Master of Public Policy in Economic Policy", "357"],
                             ["Master of Public Policy in International Policy", "358"],
                             ["Master of Public Policy in Policy Analysis", "359"],
                             ["Master of Public Policy in Social Policy", "360"],
                             ["Master of Science Communication", "361"],
                             ["Master of Science Communication", "362"],
                             ["Master of Science Communication Outreach", "363"],
                             ["Master of Science in Science Communication", "364"],
                             ["Master of Social Research", "365"],
                             ["Master of Social Research (Advanced)", "366"],
                             ["Master of Statistics", "367"],
                             ["Master of Strategic Studies", "368"],
                             ["Master of Strategic Studies (Advanced)", "369"],
                             ["Master of Studies", "370"],
                             ["Master of Studies (Advanced)", "371"],
                             ["Master of Translation", "372"],
                             ["Master of Translation (Advanced)", "373"],
                             ["Master of Visual Arts", "374"],
                             ["Master of Visual Arts (Advanced)", "375"],
                             ["Non Award (ANU College of Business and Economics)", "376"],
                             ["Non Award (Clinical Experience)", "377"],
                             ["Non Award Cross Institutional", "378"],
                             ["Non Award Cross-Institutional (ANU College of Business and Economics)", "379"],
                             ["Non Award Exchange Program", "380"],
                             ["Non Award Exchange Program (12 Months)", "381"],
                             ["Non Award Exchange Program (6 Months)", "382"],
                             ["Non-Award (ANU College of Asia and the Pacific)", "383"],
                             ["Non-Award (ANU College of Engineering and Computer Science)", "384"],
                             ["Non-Award (ANU Colleges of Science)", "385"],
                             ["Non-Award (ANU Medical School)", "386"],
                             ["Non-Award Arts (ANU College of Arts and Social Sciences)", "387"],
                             ["Non-Award Cross-Institutional (ANU College of Arts and Social Sciences)", "388"],
                             ["Non-Award Cross-Institutional (ANU College of Asia and the Pacific)", "389"],
                             ["Non-Award Cross-Institutional (ANU College of Engineering and Computer Science)", "390"],
                             ["Non-Award Cross-Institutional (ANU College of Law)", "391"],
                             ["Non-Award Cross-Institutional (ANU Colleges of Science)", "392"],
                             ["Non-Award Cross-Institutional National Institute of the Arts/University of Canberra", "393"],
                             ["Non-Award Law (ANU College of Law)", "394"],
                             ["Non-Award Study Abroad Program (12 Months)", "395"],
                             ["Non-Award Study Abroad Program (6 Months)", "396"],
                             ["Other", "397"]]});

    add_question(questionMap,
                 Question_Type.Radio,
                 "Do you know Neo-Plasticism style painting?",
                 "It is also known as De Stijl. Do you know this painting style before?",
                 {"values": ["Yes", "No"]});
    questionMap["questionInstructionTitle"]='\"Part 1 - Basic Questions\"';
    questionMap['questionInstructionText'] = '"In this part, you have to answer several questions which related to your personal information. Before you answer these questions, make sure that you have read, understood and signed the <i>Participant Information Sheet</i>.</p><p>The following questions will collect your ANU ID, gender, age and college. If you feel that some of those details which you do not want to share with us, you can quit this experiment now.</p><p>Click \'start\' when you are ready."'
    return render_question_page(request, questionMap);

@csrf_exempt
def generate_iteration_images(request):
    # Check the result.
    if(request.method=="POST"):
        post_data=request.POST;
        exp_result=post_data["exp_result"];
        last_result=json.loads(exp_result);
        uid=post_data["uid"];
        iteration=post_data["iteration"];
        # Check the iteration.
        iteration=int(iteration);
        if iteration==len(multiple_ui)-1:
            return JsonResponse({"state":"complete"});
        image_score_list=[];
        for i in range(0, 27):
            image_score_list.append(0);
        # change exp_result to structure.
        if isinstance(last_result, list):
            # initial iteration.
            for i in last_result:
                image_path=i['image'][14:];
                dot_pos=image_path.index('.');
                image_path=image_path[0:dot_pos];
                image_score_list[int(image_path)-1]=i['score'];
        else:
            # last result is class, iteration 0 above
            last_result=last_result["result"];
            for i in last_result:
                image_path=i['image'][len(uid)+22+len(str(iteration)):];
                dot_pos=image_path.index('.');
                image_path=image_path[0:dot_pos];
                image_score_list[int(image_path)]=int(i['score']);
        # Increase the iteration
        iteration=str(iteration+1);
        # Generate the file name list.
        BASE = os.path.dirname(os.path.abspath(__file__));
        imageFilename=[];
        iteration_image_list=[];
        for i in range(0, 27):
            imagePath="static/hash_images/"+uid+"-i"+iteration+"-"+str(i)+".png";
            iteration_image_list.append(imagePath);
            imageFilename.append(os.path.join(BASE, imagePath));
        # Generate the image.
        last_gene=json.loads(post_data["image_gene"]);
        iteration_generator=imageGenerator();
        last_gene=iteration_generator.generate_iteration(last_gene, imageFilename, image_score_list);
        iteration_gene=json.dumps(last_gene);
        # Save the last gene to a exp data.
        gene_title=uid+"|iteration"+iteration+"-gene";
        searchList=ExpResult.objects.filter(title=gene_title);
        if(len(searchList)!=0):
            searchList[0].result=iteration_gene;
            searchList[0].save();
        else:
            exp_result = ExpResult(result=iteration_gene, title=gene_title);
            exp_result.save();
        return JsonResponse({'state':'ok',
                             'uid':uid,
                             'iteration':iteration});
    return start_question;

@csrf_exempt
def send_question_result(request):
    # Check the result.
    if(request.method=="POST"):
        post_data=request.POST;
        exp_result=post_data["exp_result"];
        question_result=json.loads(exp_result);
        uid=question_result[0];
        title=uid+"|info";
        searchList=ExpResult.objects.filter(title=title);
        if(len(searchList)!=0):
            searchList[0].result=exp_result;
            searchList[0].save();
        else:
            exp_result = ExpResult(result=exp_result, title=title);
            exp_result.save();
        return JsonResponse({'state':'ok', 'uid':uid});
    return start_question;

@csrf_exempt
def send_initial(request):
    # Check the result.
    if(request.method=="POST"):
        post_data=request.POST;
        exp_result=post_data["exp_result"];
        uid=post_data["uid"];
        title=uid+"|initial";
        searchList=ExpResult.objects.filter(title=title);
        if(len(searchList)!=0):
            searchList[0].result=exp_result;
            searchList[0].save();
        else:
            exp_result = ExpResult(result=exp_result, title=title);
            exp_result.save();
        return JsonResponse({'state':'ok', 'uid':uid});
    return start_single_choices(request);

@csrf_exempt
def send_iteration(request):
    # Check the result.
    if(request.method=="POST"):
        post_data=request.POST;
        exp_result=post_data["exp_result"];
        uid=post_data["uid"];
        iteration=post_data["iteration"];
        title=uid+"|iteration-"+iteration;
        searchList=ExpResult.objects.filter(title=title);
        if(len(searchList)!=0):
            searchList[0].result=exp_result;
            searchList[0].save();
        else:
            exp_result = ExpResult(result=exp_result, title=title);
            exp_result.save();
        return JsonResponse({'state':'ok', 'uid':uid});
    return start_multiple_choices(request);
