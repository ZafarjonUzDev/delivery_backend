# from django.urls import path
# from .views import CategoryListView, ProductDetailView, ProductListView

# app_name = 'catalog'

# urlpatterns = [
#     path('categories/', CategoryListView.as_view(), name='category_list'),
#     path('products/', ProductListView.as_view(), name='product_list'),
#     path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
# ]


"""
Catalog Management URL Configuration.

Mahsulotlar katalogi hamda kategoriyalarni boshqarish bo'limi.

Endpoints:
- Categories: GET /api/v1/catalog/categories/
- Products:   GET /api/v1/catalog/products/
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet

app_name = 'catalog'

# Enterprise Catalog Resource Router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]