from django.urls import path
from .views import MainPage, Destination

urlpatterns = [
    path('', MainPage.as_view(), name="main_page"),
    path('destination/<slug:category_slug>', Destination.as_view(), name="destination"),
]
