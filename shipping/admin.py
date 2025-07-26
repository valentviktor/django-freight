from django.contrib import admin
from .models import Country, Category

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_currency', 'country_flag')
    search_fields = ('country_name', 'country_currency')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title', 'country', 'price_per_kilo')
    list_filter = ('country',)
    search_fields = ('category_title',)
    autocomplete_fields = ('country',)