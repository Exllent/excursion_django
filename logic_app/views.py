from django.db.models import QuerySet
from django.http import HttpResponseNotFound, HttpRequest, HttpResponse, JsonResponse
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View
from django.contrib import messages
from .models import Category, Excursion, Booking, Review, GalleryReview
from .forms import BookingForm
from .tasks import send_message_in_chat_tg
from .utils import current_datetime_msk


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

    @staticmethod
    def get_context(excursion_slug):
        tour_cache = cache.get(excursion_slug)
        if tour_cache:
            return tour_cache
        else:
            excursion = get_object_or_404(Excursion.get_tour_with_locations_by_slug(excursion_slug))
            reviews = excursion.reviews.order_by('-created_at').all()
            context = {
                "excursion": excursion,
                "locations": excursion.location.all(),
                "reviews": reviews[:3],
                "len_reviews": len(reviews),
                "has_more": True if len(reviews) > 3 else False
            }
            cache.set(excursion_slug, context, 60 * 10)
            return context

    def get(self, request: HttpRequest, excursion_slug: str):
        context = self.get_context(excursion_slug)
        context['form'] = BookingForm()
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, excursion_slug: str):
        form = BookingForm(request.POST)
        if form.is_valid():
            ex = Excursion.get_excursion_by_slug(excursion_slug)
            data = form.cleaned_data
            number_words = {
                1: 'один человек',
                2: 'двое человек',
                3: 'трое человек',
                4: 'четверо человек',
                5: 'пятеро человек',
                6: 'шестеро человек',
                7: 'семеро человек',
                8: 'восемеро человек',
                9: 'девятеро человек',
                10: 'десятеро человек',
                11: 'более десяти человек'
            }
            send_message_in_chat_tg.delay(
                f"Экскурсия: {ex.title}\n"
                f"Цена : {ex.price}\n"
                f"Имя: {data['name']}\n"
                f"Дата : {data['date_excursion']}\n"
                f"Номер : {data['number_phone']}\n"
                f"Количество : {number_words[data['people']]}\n"
                f"Пожелание: {'Без пожелания' if len(data['wishes']) == 0 else data['wishes']}"
            )
            message = (
                f"{data['name']}, вы успешно забронировали {'места' if data['people'] > 1 else 'место'} на экскурсию {ex.title}. "
                f"Скоро с вами свяжется наш туроператор, желаем вам хорошего время провождения! "
                f"С уважением, команда ЭТОСИРИУС.\n\n"
                f"Кстати, у нас есть множество других захватывающих экскурсий, которые также могут вас заинтересовать. "
                f"Не забудьте снова заглянуть на наш сайт, чтобы узнать больше!"
            )
            booking = Booking.objects.create_booking(
                name=data['name'],
                phone_number=data['number_phone'],
                number_of_people=data['people'],
                wishes=data['wishes'],
                user_agent=request.META.get("HTTP_USER_AGENT", "unknown"),
                created_at=current_datetime_msk(),
                excursion=ex
            )
            booking.save()
            messages.success(request, message)
            return redirect('excursion', excursion_slug=excursion_slug)
        else:
            context = self.get_context(excursion_slug)
            context['form'] = form
            return render(request, template_name=self.template_name, context=context)


def load_more_reviews(request):
    slug = request.GET.get('slug')
    page = int(request.GET.get('page', 1))
    reviews_per_page = 3
    offset = (page - 1) * reviews_per_page

    excursion = Excursion.objects.get(slug=slug)
    reviews = Review.objects.filter(excursion_id=excursion.id).order_by('-created_at')[offset:offset + reviews_per_page]

    reviews_list = [{
        'name': review.name,
        'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'review': review.review,
    } for review in reviews]

    has_more = reviews.count() == reviews_per_page
    return JsonResponse({'reviews': reviews_list, 'has_more': has_more})


class GalleryReviews(ListView):
    template_name = "logic_app/reviews.html"
    model = GalleryReview
    context_object_name = "reviews"


def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="logic_app/about.html", context={"title": "О нас"})


def page_not_found(request, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(request, exception)
