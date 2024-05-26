from django.urls import path
from .views import MainPage, Destination, Tours, ShowTour, about_us, load_more_reviews

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('about_us', about_us, name='about_us'),
    path('excursion', Tours.as_view(), name='all_excursion'),
    path('<slug:excursion_slug>', ShowTour.as_view(), name='excursion'),
    path('load-more-reviews/', load_more_reviews, name='load_more_reviews'),
    path('destination/<slug:category_slug>', Destination.as_view(), name='destination'),
]
