from django.db.models import QuerySet
from django.http import HttpResponseNotFound, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import Category, Excursion
from .forms import Application


class MainPage(ListView):
    template_name = "logic_app/index.html"
    context_object_name = "context_data"
    extra_context = {'title': 'Главная страница'}

    def get_queryset(self) -> dict[str: QuerySet]:
        return {
            "excursions": Excursion.get_tours_with_count_location(),
            "categories": Category.get_categories_with_counts()
        }


class Destination(ListView):
    template_name = "logic_app/package.html"
    context_object_name = "excursions"
    extra_context = {'title': 'Популярные направления'}

    def get_queryset(self) -> QuerySet:
        return Excursion.get_tours_by_category_slug(slug=self.kwargs["category_slug"])


class Tours(ListView):
    template_name = "logic_app/package.html"
    queryset = Excursion.published.all()
    context_object_name = "excursions"


class ShowTour(View):
    template_name = "logic_app/excursion.html"

    def get(self, request: HttpRequest, excursion_slug: str):
        excursion = get_object_or_404(Excursion.get_tour_with_locations_by_slug(excursion_slug))
        context = {
            "excursion": excursion,
            "locations": excursion.location.all(),
            "form": Application()
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, excursion_slug: str):
        form = Application(request.POST)
        if form.is_valid():
            print(form.cleaned_data, 'sssssssssssssssssssssssssss')
            print(excursion_slug, 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
        else:
            print(form.errors)
        return HttpResponse("<h1>Hello<h1/>")


def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="logic_app/about.html")


def page_not_found(request, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(request, exception)
