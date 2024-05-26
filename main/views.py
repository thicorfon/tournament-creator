from django.http import HttpResponse
from django.shortcuts import render

def hi(request):
    return HttpResponse("<h1>HI</h1>")# Create your views here.
