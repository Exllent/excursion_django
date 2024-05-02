from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views.generic import ListView
from .models import Category, Excursion


class MainPage(ListView):
    template_name = "logic_app/index.html"
    queryset = Category.categories_with_excursion_data()
    context_object_name = "categories"


class Destination(ListView):
    template_name = "logic_app/destination.html"
    model = Category
    queryset = Category.get_categories_with_counts()
    context_object_name = "categories"


def page_not_found(request, exception):
    return HttpResponseNotFound(request, exception)
