import os
import requests
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Country, Category
from .serializers import CountrySerializer, CategorySerializer

class CountryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', '')
        countries = Country.objects.filter(country_name__icontains=search_query)
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        country_id = request.query_params.get('country_id')
        search_query = request.query_params.get('search', '')

        if not country_id:
            return Response({"error": "country_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        categories = Category.objects.filter(
            country_id=country_id,
            category_title__icontains=search_query
        )
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class DestinationCityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        api_key = os.getenv('RAJAONGKIR_API_KEY')
        url = "https://api.rajaongkir.com/starter/city"
        headers = {'key': api_key}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            cities = data.get('rajaongkir', {}).get('results', [])
            return Response(cities)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to connect to RajaOngkir: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CalculateFreightAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        country_id = request.data.get('country_id')
        category_id = request.data.get('category_id')
        destination_id = request.data.get('destination_id')
        weight_kg = request.data.get('weight')

        if not all([country_id, category_id, destination_id, weight_kg]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            country = Country.objects.get(id=country_id)
            category = Category.objects.get(id=category_id, country=country)
            weight_grams = int(Decimal(weight_kg) * 1000)

            international_price = Decimal(weight_kg) * category.price_per_kilo

            api_key = os.getenv('RAJAONGKIR_API_KEY')
            url = "https://api.rajaongkir.com/starter/cost"
            headers = {'key': api_key, 'content-type': 'application/x-www-form-urlencoded'}
            
            payload = {
                'origin': '152', 
                'destination': str(destination_id),
                'weight': str(weight_grams),
                'courier': 'jne'
            }
            
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            domestic_data = response.json()

            costs = domestic_data.get('rajaongkir', {}).get('results', [{}])[0].get('costs', [])
            if not costs:
                return Response({"error": "Domestic shipping to the destination is not available."}, status=status.HTTP_404_NOT_FOUND)
            
            domestic_price = Decimal(costs[0]['cost'][0]['value'])

            total_price = international_price + domestic_price

            response_data = {
                "origin": country.country_name,
                "destination_city_id": destination_id,
                "category_name": category.category_title,
                "weight_kg": weight_kg,
                "international_price": f"{international_price:.2f}",
                "domestic_price": f"{domestic_price:.2f}",
                "total_price": f"{total_price:.2f}",
                "currency": "IDR"
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Country.DoesNotExist:
            return Response({"error": "Invalid country_id."}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({"error": "Invalid category_id for the selected country."}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to calculate domestic shipping: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)