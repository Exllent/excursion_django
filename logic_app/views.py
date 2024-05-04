from django.db.models import QuerySet
from django.http import HttpResponseNotFound, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from .models import Category, Excursion


class MainPage(ListView):
    template_name = "logic_app/index.html"
    queryset = Category.get_categories_with_counts()
    context_object_name = "categories"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.get_categories_with_counts()
        context["excursion"] = Excursion.get_tours_with_count_location()
        return context


class Destination(ListView):
    template_name = "logic_app/package.html"
    # queryset = Excursion.objects.all()
    context_object_name = "excursion"

    def get_queryset(self) -> QuerySet:
        return Excursion.get_tours_by_category_slug(slug=self.kwargs["category_slug"])


class Tours(ListView):
    template_name = "logic_app/package.html"
    queryset = Excursion.published.all()
    context_object_name = "excursion"


def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="logic_app/about.html")


def page_not_found(request, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(request, exception)
