# from django.shortcuts import render

# # Create your views here.

# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from .models import Order
# from .serializers import OrderCreateSerializer, OrderSerializer


# class OrderListCreateView(generics.ListCreateAPIView):
#     """
#     GET: Foydalanuvchining o'z buyurtmalari ro'yxati.
#     POST: Yangi buyurtma yaratish.
#     """

#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         # Faqat tizimga kirgan foydalanuvchining buyurtmalarini qaytaradi
#         return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return OrderCreateSerializer
#         return OrderSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         order = serializer.save()

#         response_serializer = OrderSerializer(order)
#         return Response(response_serializer.data, status=status.HTTP_201_CREATED)


# class OrderDetailView(generics.RetrieveAPIView):
#     """Buyurtma tafsilotlarini ko'rish."""

#     permission_classes = (IsAuthenticated,)
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer
)
from .services import create_order


class OrderViewSet(viewsets.ModelViewSet):
    """
    Buyurtmalarni boshqarish va ko'rish uchun yuqori unumdorlikka ega (High-Performance) ViewSet.
    
    Features:
    - Customer faqat o'ziga tegishli buyurtmalarni ko'radi va yaratadi.
    - Database Optimization: 'prefetch_related' orqali N+1 so'rovlar bartaraf etilgan.
    - Clean Architecture: Buyurtma yaratish 'services.py' atomik servisi orqali bajariladi.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Database Query Optimization:
        Faqat joriy foydalanuvchining buyurtmalarini 'prefetch_related' bilan 
        bitta samarali SQL so'rovda olib keladi.
        """
        user = self.request.user
        base_queryset = Order.objects.prefetch_related('items__product')
        
        if user.is_staff:
            return base_queryset.all()
        return base_queryset.filter(customer=user)

    def get_serializer_class(self):
        """
        So'rov turiga (action) qarab mos serializer'ni qaytaradi:
        - GET /orders/ -> OrderListSerializer (Yengil ro'yxat)
        - GET /orders/{id}/ -> OrderDetailSerializer (To'liq chek)
        - POST /orders/ -> OrderCreateSerializer (Input validation)
        """
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        """
        Clean Architecture:
        1. Input ma'lumotlarni OrderCreateSerializer orqali validatsiya qiladi.
        2. Yaratish logikasini 'create_order' atomik servisiga uzatadi.
        3. Tayyor buyurtmani OrderDetailSerializer orqali to'liq chek shaklida qaytaradi.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Input data
        validated_data = serializer.validated_data
        
        # Atomik servisni chaqirish
        order = create_order(
            customer=request.user,
            delivery_phone_number=validated_data['delivery_phone_number'],
            delivery_address=validated_data['delivery_address'],
            items_data=validated_data['items'],
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude')
        )

        # Qaytariladigan javob uchun Detail Serializer ishlatiladi
        response_serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)