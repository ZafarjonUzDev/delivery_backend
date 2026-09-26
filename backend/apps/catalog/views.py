# from django.shortcuts import render

# # Create your views here.

# from rest_framework import generics
# from rest_framework.permissions import AllowAny

# from .models import Category, Product
# from .serializers import CategorySerializer, ProductSerializer


# class CategoryListView(generics.ListAPIView):
#     """Barcha faol kategoriyalar ro'yxati."""

#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = (AllowAny,)


# class ProductListView(generics.ListAPIView):
#     """Barcha sotuvda bor mahsulotlar ro'yxati va filterlash."""

#     serializer_class = ProductSerializer
#     permission_classes = (AllowAny,)

#     def get_queryset(self):
#         queryset = Product.objects.filter(is_available=True)
#         category_id = self.request.query_params.get('category')
#         if category_id:
#             queryset = queryset.filter(category_id=category_id)
#         return queryset


# class ProductDetailView(generics.RetrieveAPIView):
#     """Mahsulot haqida batafsil ma'lumot."""

#     queryset = Product.objects.filter(is_available=True)
#     serializer_class = ProductSerializer
#     permission_classes = (AllowAny,)
#     lookup_field = 'slug'


from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product
from .serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductWriteSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Kategoriyalarni boshqarish va ko'rish uchun ViewSet.
    
    - Customer / Anonim: Barcha faol kategoriyalar va ularning tafsilotlarini ko'ra oladi (GET).
    - Manager / Admin: Yangi kategoriya yaratish, tahrirlash va o'chirish huquqiga ega.
    """
    queryset = Category.objects.filter(is_active=True)

    def get_permissions(self):
        """O'qish (GET) so'rovlari uchun barchaga ruxsat, yozish (POST/PUT/DELETE) uchun faqat Admin/Manager."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Action'ga qarab yengil List yoki batafsil Detail serializer qaytaradi."""
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategoryListSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Mahsulotlar katalogi uchun yuqori unumdorlikka ega (High-Performance) ViewSet.
    
    Features:
    - N+1 so'rovlar muammosini bartaraf etish uchun 'select_related' ishlatilgan.
    - Kategoriya bo'yicha filtrlash va nom bo'yicha qidiruv (Search) integratsiya qilingan.
    - So'rov turiga (GET list, GET detail, POST/PUT) qarab mos serializer avtomatik tanlanadi.
    """
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Database Query Optimization:
        'select_related' orqali mahsulot bilan birga uning kategoriyasini ham 1 ta SQL so'rovda olib keladi.
        Manager barcha mahsulotlarni, mijozlar esa faqat 'is_available=True' bo'lganlarini ko'radi.
        """
        user = self.request.user
        base_queryset = Product.objects.select_related('category')
        
        if user.is_authenticated and user.is_staff:
            return base_queryset.all()
        return base_queryset.filter(is_available=True)

    def get_permissions(self):
        """O'qish barchaga ochiq, yarata olish va tahrirlash faqat Manager/Admin uchun."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Arxitektura bo'yicha serializer ajratish:
        - GET /products/ -> ProductListSerializer (Yengil payload)
        - GET /products/{id}/ -> ProductDetailSerializer (To'liq tafsilot)
        - POST / PUT / PATCH -> ProductWriteSerializer (Manager CUD amallari)
        """
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductWriteSerializer