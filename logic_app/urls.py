from django.urls import path
from .views import TopDestination

urlpatterns = [
    path('', TopDestination.as_view(), name="main_page")
]
