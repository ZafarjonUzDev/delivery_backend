# from django.db import models
# from django.conf import settings
# from decimal import Decimal

# from apps.catalog.models import Product


# # Create your models here.
# """
# Orders app uchun ma'lumotlar bazasi modellari.

# Ushbu modul foydalanuvchilarning buyurtmalari (Order) hamda buyurtma tarkibidagi
# mahsulotlar (OrderItem) hayotiy tsiklini boshqarish uchun xizmat qiladi.
# """


# class Order(models.Model):
#     """
#     Foydalanuvchi buyurtmasining umumiy ma'lumotlari va hayotiy tsikli (statusi).

#     Buyurtmachi, yetkazib berish manzili, geolokatsiya (latitude/longitude),
#     aloqa uchun telefon raqami hamda umumiy to'lov summasini saqlaydi.
#     """

#     class StatusChoices(models.TextChoices):
#         PREPARING = 'preparing', 'Tayyorlanmoqda'
#         IN_TRANSIT = 'in_transit', "Yo'lda"
#         DELIVERED = 'delivered', 'Yetkazib berildi'
#         CANCELLED = 'cancelled', 'Bekor qilindi'

#     customer = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT,
#         related_name='orders',
#         verbose_name="Buyurtmachi (Akkount)",
#         help_text="Buyurtmani amalga oshirgan foydalanuvchi akkounti."
#     )
#     delivery_phone_number = models.CharField(
#         max_length=20,
#         verbose_name="Muloqot uchun tel. raqam",
#         help_text="Kuryer bog'lanishi uchun mo'ljallangan telefon raqami."
#     )
#     total_amount = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         default=0.00,
#         verbose_name="Umumiy summa",
#         help_text="Buyurtmaning barcha mahsulotlari va xizmatlarining umumiy narxi."
#     )
#     status = models.CharField(
#         max_length=20,
#         choices=StatusChoices.choices,
#         default=StatusChoices.PREPARING,
#         verbose_name="Holati",
#         help_text="Buyurtmaning hozirgi bosqichi."
#     )
#     delivery_address = models.TextField(
#         verbose_name="Yetkazib berish manzili",
#         help_text="Foydalanuvchi tomonidan kiritilgan matnli manzil."
#     )
#     latitude = models.DecimalField(
#         max_digits=9,
#         decimal_places=6,
#         null=True,
#         blank=True,
#         verbose_name="Kenglik (Latitude)",
#         help_text="Xaritadagi GPS kenglik koordinatasi."
#     )
#     longitude = models.DecimalField(
#         max_digits=9,
#         decimal_places=6,
#         null=True,
#         blank=True,
#         verbose_name="Uzoqlik (Longitude)",
#         help_text="Xaritadagi GPS uzoqlik koordinatasi."
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name="Yaratilgan vaqti"
#     )
#     updated_at = models.DateTimeField(
#         auto_now=True,
#         verbose_name="Yangilangan vaqti"
#     )

#     class Meta:
#         verbose_name = "Buyurtma"
#         verbose_name_plural = "Buyurtmalar"
#         ordering = ['-created_at']

#     def __str__(self) -> str:
#         return f"Order #{self.id} - {self.delivery_phone_number} ({self.get_status_display()})"


# class OrderItem(models.Model):
#     """
#     Buyurtma tarkibidagi yakka mahsulot pozitsiyasi.

#     Eslatma: 'price' maydoni sotib olingan vaqtdagi narxni snapshot (fiksatsiya)
#     qilib saqlaydi. Bu mahsulotning katalogdagi kelajakdagi narx o'zgarishlari
#     eski buyurtmalar tarixiga ta'sir qilmasligini ta'minlaydi.
#     """

#     order = models.ForeignKey(
#         Order,
#         on_delete=models.CASCADE,
#         related_name='items',
#         verbose_name="Buyurtma",
#         help_text="Mahsulot tegishli bo'lgan asosiy buyurtma."
#     )
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.PROTECT,
#         related_name='order_items',
#         verbose_name="Mahsulot",
#         help_text="Sotib olinayotgan katalogdagi mahsulot."
#     )
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         verbose_name="Sotib olingan paytdagi narxi",
#         help_text="Buyurtma berilgan vaqtdagi bir birlik mahsulot narxi."
#     )
#     quantity = models.PositiveIntegerField(
#         default=1,
#         verbose_name="Soni",
#         help_text="Xarid qilingan mahsulotlar miqdori."
#     )

#     class Meta:
#         verbose_name = "Buyurtma mahsuloti"
#         verbose_name_plural = "Buyurtma mahsulotlari"

#     def __str__(self) -> str:
#         return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"
    
#     @property
#     def total_price(self) -> Decimal:
#         """Ushbu pozitsiyadagi mahsulotning umumiy summasini hisoblaydi."""
#         return self.price * self.quantity


from decimal import Decimal
from django.db import models
from django.conf import settings

from apps.catalog.models import Product


class Order(models.Model):
    """
    Foydalanuvchi buyurtmasining umumiy ma'lumotlari va hayotiy tsikli (statusi).

    Enterprise Standard:
    - Status va Yaratilgan vaqti bo'yicha tezkor filterlash uchun 'db_index=True' qo'llanilgan.
    - Buyurtmachi, yetkazib berish manzili va GPS koordinatlarini saqlaydi.
    """

    class StatusChoices(models.TextChoices):
        PREPARING = 'preparing', 'Tayyorlanmoqda'
        IN_TRANSIT = 'in_transit', "Yo'lda"
        DELIVERED = 'delivered', 'Yetkazib berildi'
        CANCELLED = 'cancelled', 'Bekor qilindi'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name="Buyurtmachi (Akkount)",
        help_text="Buyurtmani amalga oshirgan foydalanuvchi akkounti."
    )
    delivery_phone_number = models.CharField(
        max_length=20,
        verbose_name="Muloqot uchun tel. raqam",
        help_text="Kuryer bog'lanishi uchun mo'ljallangan telefon raqami."
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name="Umumiy summa",
        help_text="Buyurtmaning barcha mahsulotlari va xizmatlarining umumiy narxi."
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PREPARING,
        db_index=True,  # Status bo'yicha filterlarni tezlashtirish uchun
        verbose_name="Holati",
        help_text="Buyurtmaning hozirgi bosqichi."
    )
    delivery_address = models.TextField(
        verbose_name="Yetkazib berish manzili",
        help_text="Foydalanuvchi tomonidan kiritilgan matnli manzil."
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Kenglik (Latitude)",
        help_text="Xaritadagi GPS kenglik koordinatasi."
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Uzoqlik (Longitude)",
        help_text="Xaritadagi GPS uzoqlik koordinatasi."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,  # Vaqt bo'yicha saralashni tezlashtirish uchun
        verbose_name="Yaratilgan vaqti"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan vaqti"
    )

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Order #{self.id} - {self.delivery_phone_number} ({self.get_status_display()})"


class OrderItem(models.Model):
    """
    Buyurtma tarkibidagi yakka mahsulot pozitsiyasi.

    Eslatma: 'price' maydoni sotib olingan vaqtdagi narxni snapshot (fiksatsiya)
    qilib saqlaydi. Bu mahsulotning katalogdagi kelajakdagi narx o'zgarishlari
    eski buyurtmalar tarixiga ta'sir qilmasligini ta'minlaydi.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Buyurtma",
        help_text="Mahsulot tegishli bo'lgan asosiy buyurtma."
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name="Mahsulot",
        help_text="Sotib olinayotgan katalogdagi mahsulot."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Sotib olingan paytdagi narxi",
        help_text="Buyurtma berilgan vaqtdagi bir birlik mahsulot narxi."
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Soni",
        help_text="Xarid qilingan mahsulotlar miqdori."
    )

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"

    @property
    def total_price(self) -> Decimal:
        """Ushbu pozitsiyadagi mahsulotning umumiy summasini hisoblaydi."""
        return self.price * self.quantity