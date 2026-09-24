# """
# Accounts ilovasining URL yo'nalishlari (Routing).
# """

# from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView

# from .views import (
#     CustomTokenObtainPairView,
#     RegisterView,
#     UserProfileView,
# )

# app_name = 'accounts'

# urlpatterns = [
#     path('register/', RegisterView.as_dict() if hasattr(RegisterView, 'as_dict') else RegisterView.as_view(), name='register'),
#     path('login/', CustomTokenObtainPairView.as_view(), name='login'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('me/', UserProfileView.as_view(), name='user_profile'),
# ]

"""
Accounts & Authentication URL Configuration.

Foydalanuvchilarni autentifikatsiya qilish, ro'yxatdan o'tkazish
va profillarini boshqarish uchun mas'ul bo'lgan URL xaritasi.

Endpoints:
- POST /api/v1/accounts/register/       -> Yangi foydalanuvchini ro'yxatdan o'tkazish
- POST /api/v1/accounts/login/          -> JWT Access & Refresh token olish
- POST /api/v1/accounts/token/refresh/  -> Expired bo'lgan Access tokenni yangilash
- GET/PUT/PATCH /api/v1/accounts/users/ -> User Profil boshqaruvi
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    UserViewSet,
)

app_name = 'accounts'

# User Profiles Management Router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Auth & JWT Management Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile & Users Management Endpoints
    path('', include(router.urls)),
]