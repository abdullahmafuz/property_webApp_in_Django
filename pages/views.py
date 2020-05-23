from django.shortcuts import render
from django.http import HttpResponse


def index(resquest):
    return render(resquest, 'pages/index.html')


def about(resquest):
    return render(resquest, 'pages/about.html')
