from django.urls import path
from .api_views import (
    CountryListAPIView,
    CategoryListAPIView,
    DestinationCityAPIView,
    CalculateFreightAPIView,
)
from . import views

urlpatterns = [
    path('countries/', CountryListAPIView.as_view(), name='api_countries'),
    path('categories/', CategoryListAPIView.as_view(), name='api_categories'),
    path('destination/', DestinationCityAPIView.as_view(), name='api_destination'), 
    path('calculate/', CalculateFreightAPIView.as_view(), name='api_calculate'),
]
