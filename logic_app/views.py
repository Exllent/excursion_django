from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound


# Create your views here.

def index(request: HttpRequest):
    return render(request, template_name='logic_app/index.html')


def page_not_found(request, exception):
    return HttpResponseNotFound(request, exception)

