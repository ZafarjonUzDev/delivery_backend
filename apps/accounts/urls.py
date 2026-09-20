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


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    UserViewSet,
)

app_name = 'accounts'

# User va Profile boshqaruvi uchun Router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Auth Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User & Profile Endpoints (Router)
    path('', include(router.urls)),
]