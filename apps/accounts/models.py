# from django.contrib.auth.models import AbstractUser
# from django.db import models

# # Create your models here.


# class User(AbstractUser):
#     """
#     Tizimdagi barcha foydalanuvchilar (Magaer va Customer lar) uchun Custom User modeli.
#     Login qilish tel.raqami orqali amalga oshiriladi.
#     """
#     phone_number = models.CharField(
#         max_length=15,
#         unique=True,
#         verbose_name="Phone number"
#     )

#     is_manager = models.BooleanField(
#         default=False,
#         verbose_name="Is Manager"
#     )

#     is_customer = models.BooleanField(
#         default=True,
#         verbose_name="Is Customer"
#     )


#     # Login uchun username o'rniga phone_number ishlatiladi
#     USERNAME_FIELD = 'phone_number'

#     # Terminalda createsuperuser qilinganda so'raladigan qo'shimcha maydon
#     REQUIRED_FIELDS = ['username']


#     def __str__(self):
#         """Obyektni matn ko'rinishida aks ettirish (Admin panel va loglar uchun)"""
#         role = 'Manager' if self.is_manager else 'Customer'
#         return f"{self.phone_number} ({role})"


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Phone number orqali autentifikatsiya qiluvchi Custom User Manager.
    Terminalda 'createsuperuser' buyrug'i to'g'ri va xatosiz ishlashini ta'minlaydi.
    """
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Telefon raqami kiritilishi shart.")
        
        extra_fields.setdefault('is_customer', True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_customer', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser uchun is_staff=True bo\'lishi shart.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser uchun is_superuser=True bo\'lishi shart.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """
    Tizimdagi barcha foydalanuvchilar (Manager va Customer lar) uchun Custom User modeli.
    
    Enterprise Standard:
    - Login qilish phone_number orqali amalga oshiriladi.
    - Tezkor autentifikatsiya va permission tekshiruvlari uchun 'db_index=True' qo'llanilgan.
    """
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,  # Auth so'rovlarini tezlashtirish uchun
        verbose_name="Telefon raqami"
    )

    is_manager = models.BooleanField(
        default=False,
        db_index=True,  # Permission checklarini tezlashtirish uchun
        verbose_name="Manager-mi"
    )

    is_customer = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Mijoz-mi"
    )

    objects = CustomUserManager()

    # Login uchun username o'rniga phone_number ishlatiladi
    USERNAME_FIELD = 'phone_number'

    # Terminalda createsuperuser qilinganda so'raladigan maydonlar
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-date_joined']

    def __str__(self):
        """Obyektni matn ko'rinishida aks ettirish (Admin panel va loglar uchun)."""
        return f"{self.phone_number} ({self.role})"

    @property
    def role(self) -> str:
        """Foydalanuvchi rolini matn shaklida qaytaradi."""
        if self.is_superuser or self.is_manager:
            return "Manager"
        return "Customer"