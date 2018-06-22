from django.shortcuts import render
from django.http import request, HttpResponse


def home(request):
	return HttpResponse("This is the home page")

def help(request):
	return HttpResponse("This is the help page")