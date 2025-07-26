from django import forms
from .models import Country, Category

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['country_name', 'country_flag', 'country_currency']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['country', 'category_title', 'price_per_kilo']
