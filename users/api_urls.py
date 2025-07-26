from django.urls import path
from .api_views import UserRegisterAPIView, CustomAuthToken

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='api_user_register'),
    path('login/', CustomAuthToken.as_view(), name='api_user_login'),
]
