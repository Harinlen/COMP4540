from django.shortcuts import render

single_choice_codename = 'fubuki'

def start_single_choices(request):
    return render(request, single_choice_codename + '/index.html');
