from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def hello(request):
    return HttpResponse("Welcome")

