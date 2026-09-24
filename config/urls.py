# """
# URL configuration for config project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

# from django.contrib import admin
# from django.urls import include, path


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/v1/accounts/', include('apps.accounts.urls', namespace='accounts')),
#     path('api/v1/catalog/', include('apps.catalog.urls', namespace='catalog')),
#     path('api/v1/orders/', include('apps.orders.urls', namespace='orders')),
# ]


"""
Root URL Configuration for Flora Delivery Backend.

Ushbu fayl butun loyihaning markaziy routing (yo'naltirish) xaritasi hisoblanadi.
Xalqaro API standartlariga (RESTful API & OpenAPI 3.0) mos ravishda versiyalangan (v1)
hamda barcha kichik modullar (apps) va avtomatik hujjatlarni (Swagger/ReDoc) birlashtiradi.

Architecture & Security Principles:
- API Versioning: `/api/v1/` prefiksi orqali barcha biznes-mantiq ajratilgan.
- Modular Routing: Har bir app o'z URL namespace'iga ega.
- OpenAPI Integration: Drf-spectacular orqali real-vaqt rejimida avtomatlashtirilgan hujjat.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# API v1 barcha modullarini bir joyga jamlash (Modular Clean Architecture)
api_v1_patterns = [
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('catalog/', include('apps.catalog.urls', namespace='catalog')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
]

urlpatterns = [
    # Django Admin Paneli
    path('admin/', admin.site.urls),

    # Interaktiv API Hujjatlari (OpenAPI 3.0 & Swagger UI)
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API Version 1.0 Endpoint'lari
    path('api/v1/', include(api_v1_patterns)),
]

# Development rejimida static va media fayllarga ishlov berish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)