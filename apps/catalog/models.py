# from django.db import models

# # Create your models here.

# class Category(models.Model):
#     """Mahsulotlar kategoriyasi modeli"""

#     name = models.CharField(
#         max_length=100,
#         unique=True,
#         verbose_name="Kategoriya nomi")
    
#     is_active = models.BooleanField(
#         default=True,
#         verbose_name="Faolmi")
    
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name="Yaratilgan vaqti")
    

#     class Meta:
#         verbose_name = "Kategoriya"
#         verbose_name_plural = "Kategoriyalar"
#         ordering = ['name']

#     def __str__(self):
#         return self.name


# class Product(models.Model):
#     """
#     Kategoriyaga tegishli mahsulotlar modeli.
#     Soft-disable logikasi (is_available) qo'llanilgan.
#     """

#     category = models.ForeignKey(
#         Category,
#         on_delete=models.PROTECT,
#         related_name='products',
#         verbose_name="Kategoriya")
    
#     name = models.CharField(
#         max_length=150,
#         verbose_name="Mahsulot nomi")
    
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         verbose_name="Narxi")
    
#     image = models.ImageField(
#         upload_to='products/',
#         blank=True,
#         null=True,
#         verbose_name="Rasm")
    
#     is_available = models.BooleanField(
#         default=True,
#         verbose_name="Mavjudmi")
    
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name="Yaratilgan vaqti")
    
#     updated_at = models.DateTimeField(
#         auto_now=True,
#         verbose_name="Yangilangan vaqti")
    

#     class Meta:
#         verbose_name = "Mahsulot"
#         verbose_name_plural = "Mahsulotlar"
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.name} - {self.price} so'm"

from django.db import models


class Category(models.Model):
    """
    Mahsulotlar kategoriyasi modeli.
    
    Enterprise Standard: Kategoriyani o'chirmasdan soft-disable qilish uchun
    'is_active' maydonidan foydalaniladi.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kategoriya nomi"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,  # Filtratsiyani tezlashtirish uchun indeks
        verbose_name="Faolmi"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Kategoriyaga tegishli mahsulotlar modeli.
    
    Enterprise Standard: Soft-disable logikasi (is_available) qo'llanilgan.
    Eski buyurtmalar yaxlitligini saqlash uchun on_delete=PROTECT ishlatilgan.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Kategoriya"
    )
    name = models.CharField(
        max_length=150,
        db_index=True,  # Qidiruv (Search API) tez ishlashi uchun indeks
        verbose_name="Mahsulot nomi"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Narxi"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Rasm"
    )
    is_available = models.BooleanField(
        default=True,
        db_index=True,  # Faol mahsulotlarni tez saralash uchun indeks
        verbose_name="Mavjudmi"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan vaqti"
    )

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.price} so'm"