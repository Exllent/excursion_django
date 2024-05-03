from django.http import HttpResponseNotFound
from django.views.generic import ListView
from .models import Category, Excursion


class MainPage(ListView):
    template_name = "logic_app/index.html"
    queryset = Category.get_categories_with_counts()
    context_object_name = "categories"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.get_categories_with_counts()
        context["excursion"] = Excursion.objects.filter(is_published=True, top=True)
        return context


class Destination(ListView):
    template_name = "logic_app/package.html"
    # queryset = Excursion.objects.all()
    context_object_name = "excursion"

    def get_queryset(self):
        return Excursion.get_tours_by_category_slug(slug=self.kwargs["category_slug"])


class Tours(ListView):
    template_name = "logic_app/package.html"
    queryset = Excursion.published.all()
    context_object_name = "excursion"


def page_not_found(request, exception):
    return HttpResponseNotFound(request, exception)
