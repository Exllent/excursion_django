from django.urls import path
from .views import MainPage, Destination, Tours

urlpatterns = [
    path('', MainPage.as_view(), name="main_page"),
    path('excursion', Tours.as_view(), name='all_excursion'),
    path('destination/<slug:category_slug>', Destination.as_view(), name="destination"),
]
