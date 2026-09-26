# from django.urls import path
# from .views import OrderDetailView, OrderListCreateView

# app_name = 'orders'

# urlpatterns = [
#     path('', OrderListCreateView.as_view(), name='order_list_create'),
#     path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
# ]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# from .views import OrderViewSet

# app_name = 'orders'

# # Enterprise Standard: ViewSet'lar uchun avtomatik va toza URL routing
# router = DefaultRouter()
# router.register(r'', OrderViewSet, basename='order')

# urlpatterns = [
#     path('', include(router.urls)),
# ]


"""
Order Management URL Configuration.

Buyurtmalarni boshqarish va unga tegishli jarayonlarni yo'naltiruvchi fayl.

Routing Logic:
- DefaultRouter orqali `OrderViewSet` resurslari avtomatik shakllantiriladi.
- Prefix `r''` (bo'sh) qilib olingan, chunki asosiy `config/urls.py` da
  'api/v1/orders/' manzili biriktirilgan. Bu RESTful `/api/v1/orders/` clean URL hosil qiladi.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

app_name = 'orders'

# Enterprise RESTful Router
router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    # CRUD: GET /api/v1/orders/, POST /api/v1/orders/, GET /api/v1/orders/{id}/
    path('', include(router.urls)),
]