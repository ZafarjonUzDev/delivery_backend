# from django.shortcuts import render

# # Create your views here.
# """
# Accounts ilovasi uchun DRF View'lari.

# Autentifikatsiya, login, tokenni yangilash va profil boshqaruvi uchun API endpointlar.
# """

# from django.contrib.auth import get_user_model
# from rest_framework import generics, status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView

# from .serializers import (
#     CustomTokenObtainPairSerializer,
#     RegisterSerializer,
#     UserProfileSerializer,
# )

# User = get_user_model()


# class RegisterView(generics.CreateAPIView):
#     """
#     Yangi foydalanuvchini ro'yxatdan o'tkazish API'si.
    
#     POST: /api/v1/accounts/register/
#     """

#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#     permission_classes = (AllowAny,)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(
#             {
#                 "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi.",
#                 "user_id": user.id,
#             },
#             status=status.HTTP_201_CREATED,
#         )


# class CustomTokenObtainPairView(TokenObtainPairView):
#     """
#     Foydalanuvchi login qilishi va JWT tokenlar (Access & Refresh) olishi uchun API.
    
#     POST: /api/v1/accounts/login/
#     """

#     serializer_class = CustomTokenObtainPairSerializer


# class UserProfileView(generics.RetrieveUpdateAPIView):
#     """
#     Tizimga kirgan foydalanuvchining o'z profilini ko'rishi va tahrirlashi uchun API.
    
#     GET / PUT / PATCH: /api/v1/accounts/me/
#     """

#     serializer_class = UserProfileSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_object(self):
#         """So'rov yuborgan joriy foydalanuvchini qaytaradi."""
#         return self.request.user


from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsManager
from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserListSerializer,
    UserDetailSerializer
)

User = get_user_model()


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

class RegisterView(generics.CreateAPIView):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish uchun API View.
    
    POST: /api/v1/accounts/register/
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi.",
                "user": {
                    "id": user.id,
                    "phone_number": user.phone_number,
                    "role": user.role
                }
            },
            status=status.HTTP_201_CREATED,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Foydalanuvchi login qilishi va JWT tokenlar (Access & Refresh) olishi uchun API.
    
    POST: /api/v1/accounts/login/
    """
    serializer_class = CustomTokenObtainPairSerializer


# ============================================================================
# USER & PROFILE MANAGEMENT VIEWSET
# ============================================================================

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Foydalanuvchilar profili va ro'yxatini boshqarish uchun ViewSet.
    
    Features:
    - Manager'lar barcha mijozlar ro'yxatini (List API) va profil tafsilotlarini (Detail API) ko'ra oladi.
    - Har qanday autentifikatsiyadan o'tgan foydalanuvchi '/me/' endpointi orqali o'z profilini ko'ra oladi va tahrirlay oladi.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Ruxsatlar boshqaruvi:
        - '/me/' harakatida faqat login bo'lganlik talab qilinadi.
        - Barcha foydalanuvchilar ro'yxati (List/Detail) faqat Manager'lar uchun ochiq.
        """
        if self.action in ['me', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsManager]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Action'ga mos serializer tanlash:
        - List API -> UserListSerializer (Yengil)
        - Detail API va Profil -> UserDetailSerializer (To'liq)
        """
        if self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Tizimga kirgan foydalanuvchining o'z profilini ko'rishi hamda tahrirlashi uchun endpoint.
        
        GET / PUT / PATCH: /api/v1/accounts/users/me/
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(user, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)