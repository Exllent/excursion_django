from django.db.models import QuerySet
from django.http import HttpResponseNotFound, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Excursion


class MainPage(ListView):
    template_name = "logic_app/index.html"
    context_object_name = "context_data"

    def get_queryset(self) -> dict[str: QuerySet]:
        return {
            "excursions": Excursion.get_tours_with_count_location(),
            "categories": Category.get_categories_with_counts()
        }


class Destination(ListView):
    template_name = "logic_app/package.html"
    context_object_name = "excursions"

    def get_queryset(self) -> QuerySet:
        return Excursion.get_tours_by_category_slug(slug=self.kwargs["category_slug"])


class Tours(ListView):
    template_name = "logic_app/package.html"
    queryset = Excursion.published.all()
    context_object_name = "excursions"


class ShowTour(DetailView):
    template_name = "logic_app/excursion.html"
    model = Excursion
    slug_url_kwarg = 'excursion_slug'

    def get_queryset(self):
        return Excursion.get_tour_with_locations_by_slug(self.kwargs['excursion_slug'])


def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="logic_app/about.html")


def page_not_found(request, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(request, exception)
