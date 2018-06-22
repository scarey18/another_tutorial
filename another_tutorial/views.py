from django.http import request, HttpResponse

def hello(request):
	return HttpResponse("Hello world!")