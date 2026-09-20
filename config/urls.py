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
Root URL Configuration for Flora Delivery Project.
Enterprise-grade routing architecture with Swagger/OpenAPI support.
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

# API v1 Patterns
api_v1_patterns = [
    path('accounts/', include('apps.accounts.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('orders/', include('apps.orders.urls')),
]

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # OpenAPI 3.0 & Swagger Schema / Documentation
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API Version 1.0 Routing
    path('api/v1/', include(api_v1_patterns)),
]

# Debug mode'da Media va Static fayllarni uzatish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)