from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManager(BasePermission):
    """
    Faqat Manager yoki Superuser lar uchun ruxsat beruvchi permission.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_manager or request.user.is_staff or request.user.is_superuser)
        )


class IsCustomer(BasePermission):
    """
    Faqat autentifikatsiyadan o'tgan mijozlar uchun ruxsat.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.is_customer
        )


class IsManagerOrReadOnly(BasePermission):
    """
    O'qish (GET, HEAD, OPTIONS) barchaga ochiq, 
    yozish/o'zgartirish faqat Manager uchun.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_manager or request.user.is_staff)
        )