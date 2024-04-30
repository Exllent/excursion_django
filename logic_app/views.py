from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views.generic import ListView
from .models import Category, Excursion


class TopDestination(ListView):
    template_name = "logic_app/index.html"
    queryset = Category.categories_with_excursion_data()
    context_object_name = "categories"


def index(request: HttpRequest):
    return render(request, template_name='logic_app/index.html')


def page_not_found(request, exception):
    return HttpResponseNotFound(request, exception)
