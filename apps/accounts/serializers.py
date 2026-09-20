# """
# Accounts ilovasi uchun DRF Serializer'lari.

# Ushbu modul foydalanuvchilarni ro'yxatdan o'tkazish, tizimga kirish (JWT)
# va profil ma'lumotlarini boshqarish uchun validatsiya mantiqlarini saqlaydi.
# """

# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):
#     """
#     Yangi foydalanuvchini ro'yxatdan o'tkazish uchun Serializer.
    
#     Parolni tasdiqlash (password2) va parolni xavfsiz shifrlab saqlash
#     mantiqlarini o'z ichiga oladi.
#     """

#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         style={'input_type': 'password'},
#         min_length=8,
#     )
#     password2 = serializers.CharField(
#         write_only=True,
#         required=True,
#         style={'input_type': 'password'},
#     )

#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'username',
#             'phone_number',
#             'first_name',
#             'last_name',
#             'password',
#             'password2',
#         )

#     def validate(self, attrs):
#         """Kiritilgan parollarning o'zaro mosligini tekshiradi."""
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {'password': "Kiritilgan parollar bir-biriga mos kelmadi."}
#             )
#         return attrs

#     def create(self, validated_data):
#         """Foydalanuvchini yaratadi va parolini shifrlaydi."""
#         validated_data.pop('password2')
#         user = User.objects.create_user(**validated_data)
#         return user


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     """
#     SimpleJWT ning standart Login Serializer'ini kengaytirish.
    
#     Token bilan birga foydalanuvchining asosiy profil ma'lumotlarini ham qaytaradi.
#     """

#     def validate(self, attrs):
#         data = super().validate(attrs)

#         # Frontend/Mobile uchun foydalanuvchi haqida qo'shimcha ma'lumotlar
#         data['user'] = {
#             'id': self.user.id,
#             'username': self.user.username,
#             'phone_number': getattr(self.user, 'phone_number', None),
#             'first_name': self.user.first_name,
#             'last_name': self.user.last_name,
#         }
#         return data


# class UserProfileSerializer(serializers.ModelSerializer):
#     """
#     Foydalanuvchi profilini ko'rish va tahrirlash uchun Serializer.
#     """

#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'username',
#             'phone_number',
#             'first_name',
#             'last_name',
#             'date_joined',
#         )
#         read_only_fields = ('id', 'username', 'date_joined')


from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


# ============================================================================
# USER PROFILE SERIALIZERS (LIST / DETAIL)
# ============================================================================

class UserListSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchilar ro'yxati (List API) uchun yengil serializer.
    
    Managerlar uchun admin panelida mijozlar ro'yxatini tezkor chiqarishga xizmat qiladi.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'phone_number',
            'first_name',
            'last_name',
            'is_manager',
            'is_customer',
        )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi profilining to'liq ma'lumotlari (Detail API / Profile API).
    """
    class Meta:
        model = User
        fields = (
            'id',
            'phone_number',
            'first_name',
            'last_name',
            'email',
            'is_manager',
            'is_customer',
            'date_joined',
            'last_login',
        )
        read_only_fields = ('id', 'phone_number', 'is_manager', 'is_customer', 'date_joined', 'last_login')


# ============================================================================
# AUTHENTICATION & REGISTRATION SERIALIZERS
# ============================================================================

class RegisterSerializer(serializers.ModelSerializer):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish uchun Serializer.
    
    Parolni tasdiqlash va parolni shifrlash mantiqlarini o'z ichiga oladi.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = (
            'id',
            'phone_number',
            'first_name',
            'last_name',
            'password',
            'password2',
        )

    def validate(self, attrs):
        """Kiritilgan parollarning o'zaro mosligini tekshiradi."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Kiritilgan parollar bir-biriga mos kelmadi."}
            )
        return attrs

    def create(self, validated_data):
        """Foydalanuvchini yaratadi va parolini shifrlaydi."""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    SimpleJWT ning standart Login Serializer'ini kengaytirish.
    
    JWT Token payload va API javobida rolni uzatadi.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom Claims (Token ichiga rolni yozish)
        token['phone_number'] = user.phone_number
        token['is_manager'] = user.is_manager
        token['is_customer'] = user.is_customer
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Frontend/Mobile uchun login bo'lganda profil ma'lumotlarini qaytarish
        data['user'] = {
            'id': self.user.id,
            'phone_number': self.user.phone_number,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
            'is_manager': self.user.is_manager,
            'is_customer': self.user.is_customer,
        }
        return data