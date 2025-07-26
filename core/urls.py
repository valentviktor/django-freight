from django.contrib import admin
from django.urls import path, include
from users.views import register_view, login_view, logout_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Monolith
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('shipping/', include('shipping.urls')),

    # API
    path('api/users/', include('users.api_urls')),
    path('api/shipping/', include('shipping.api_urls')),
]
