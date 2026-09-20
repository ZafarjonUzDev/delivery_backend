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


from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

app_name = 'orders'

# Standard RESTful Resource Routing
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]