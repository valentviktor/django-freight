from django.shortcuts import render, redirect, get_object_or_404
from .models import Country, Category
from .forms import CountryForm, CategoryForm

def country_list(request):
    countries = Country.objects.all()
    return render(request, 'dashboard/country/index.html', {'countries': countries})

def country_create(request):
    form = CountryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('country_list')
    return render(request, 'dashboard/country/form.html', {'form': form})

def country_update(request, pk):
    country = get_object_or_404(Country, pk=pk)
    form = CountryForm(request.POST or None, instance=country)
    if form.is_valid():
        form.save()
        return redirect('country_list')
    return render(request, 'dashboard/country/form.html', {'form': form})

def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        country.delete()
        return redirect('country_list')
    return render(request, 'dashboard/country/confirm-delete.html', {'object': country})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category/index.html', {'categories': categories})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'dashboard/category/form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'dashboard/category/form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'dashboard/category/confirm-delete.html', {'object': category})
