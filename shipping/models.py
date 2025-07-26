from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=100, unique=True, help_text="Name of the country")
    country_flag = models.URLField(max_length=255, blank=True, null=True, help_text="URL to the country's flag image")
    country_currency = models.CharField(max_length=10, help_text="3-letter currency code (e.g., IDR, SGD)")

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['country_name']

    def __str__(self):
        return self.country_name


class Category(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='categories', help_text="The origin country for this category")
    category_title = models.CharField(max_length=150, help_text="Title of the shipping category (e.g., Electronics, Garments)")
    price_per_kilo = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per kilogram in the country's local currency")

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('country', 'category_title') # Pastikan kategori unik per negara
        ordering = ['country__country_name', 'category_title']

    def __str__(self):
        return f"{self.category_title} ({self.country.country_name})"
