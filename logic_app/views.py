from django.db.models import QuerySet
from django.http import HttpResponseNotFound, HttpRequest, HttpResponse
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import Category, Excursion
from .forms import Application


class MainPage(ListView):
    template_name = "logic_app/index.html"
    context_object_name = "context_data"
    extra_context = {'title': 'Главная страница экскурсий в Сочи'}

    def get_queryset(self) -> dict[str: QuerySet]:
        cache_main_page = cache.get("main_page")
        if cache_main_page:
            return cache_main_page
        else:
            query_set = {
                "excursions": Excursion.get_tours_with_count_location(),
                "categories": Category.get_categories_with_counts()
            }
            cache.set("main_page", query_set, 60 * 10)
            return query_set


class Destination(ListView):
    template_name = "logic_app/package.html"
    context_object_name = "excursions"
    extra_context = {'title': 'Направления экскурсий в Сочи'}

    def get_queryset(self) -> QuerySet:
        cache_destination = cache.get(self.kwargs["category_slug"])
        if cache_destination:
            return cache_destination
        else:
            query_set = Excursion.get_tours_by_category_slug(slug=self.kwargs["category_slug"])
            cache.set(self.kwargs["category_slug"], query_set, 60 * 10)
            return query_set


class Tours(ListView):
    template_name = "logic_app/package.html"
    # queryset = Excursion.published.all()
    context_object_name = "excursions"
    extra_context = {'title': 'Экскурсии в Сочи'}
    paginate_by = 6

    def get_queryset(self):
        tours_cache = cache.get("tours")
        if tours_cache:
            return tours_cache
        else:
            query_set = Excursion.published.all()
            cache.set("tours", query_set, 60 * 10)
            return query_set


class ShowTour(View):
    template_name = "logic_app/excursion.html"

    def get(self, request: HttpRequest, excursion_slug: str):
        tour_cache = cache.get(excursion_slug)
        if tour_cache:
            tour_cache["form"] = Application()
            return render(request, self.template_name, tour_cache)
        else:
            excursion = get_object_or_404(Excursion.get_tour_with_locations_by_slug(excursion_slug))
            context = {
                "excursion": excursion,
                "locations": excursion.location.all(),
            }
            cache.set(excursion_slug, context, 60 * 10)
            context["form"] = Application()
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
    return render(request, template_name="logic_app/about.html", context={"title": "О нас"})


def page_not_found(request, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(request, exception)
