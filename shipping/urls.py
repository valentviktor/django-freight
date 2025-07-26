from django.urls import path
from . import views

urlpatterns = [
    path('countries/', views.country_list, name='country_list'),
    path('countries/create/', views.country_create, name='country_create'),
    path('countries/<int:pk>/edit/', views.country_update, name='country_update'),
    path('countries/<int:pk>/delete/', views.country_delete, name='country_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
