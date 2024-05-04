from django.urls import path
from .views import MainPage, Destination, Tours, about_us

urlpatterns = [
    path('', MainPage.as_view(), name="main_page"),
    path('about_us', about_us, name='about_us'),
    path('excursion', Tours.as_view(), name='all_excursion'),
    path('destination/<slug:category_slug>', Destination.as_view(), name="destination"),
]
