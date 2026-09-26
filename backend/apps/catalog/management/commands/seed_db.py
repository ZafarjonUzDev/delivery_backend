import logging
from decimal import Decimal
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem

User = get_user_model()
logger = logging.getLogger('django')


class Command(BaseCommand):
    """
    Flora Delivery loyihasi uchun ma'lumotlar bazasini boshlang'ich test
    ma'lumotlari bilan to'ldiruvchi avtomatlashtirilgan Custom Management Command.

    Enterprise Standartlari:
    - Idempotency: Buyruq necha marta bajarilishidan qat'i nazar, ma'lumotlar takrorlanmaydi.
    - Transactional Integrity: Barcha jarayon bitta atomik tranzaksiyada bajariladi.
    """

    help = "Baza uchun test ma'lumotlarini (Manager, Customer, Catalog, Products, Orders) yuklaydi."

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("🌱 Database Seeding jarayoni boshlandi..."))

        try:
            manager, customer = self._seed_users()
            products = self._seed_catalog()
            self._seed_orders(customer=customer, products=products)

            self.stdout.write(self.style.SUCCESS("✅ Database Seeding muvaffaqiyatli yakunlandi!"))

        except Exception as e:
            logger.error(f"Seeding jarayonida xatolik yuz berdi: {str(e)}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"❌ Seeding xatosi: {str(e)}"))

    def _seed_users(self) -> tuple[Any, Any]:
        """Manager va Customer foydalanuvchilarini yaratish."""
        self.stdout.write("  -> Foydalanuvchilar (Manager va Customer) yaratilmoqda...")

        # 1. Admin / Manager User
        manager, created = User.objects.get_or_create(
            phone_number="+998901234567",
            defaults={
                'username': "+998901234567",  # AbstractUser DB constraint uchun
                'first_name': 'System',
                'last_name': 'Manager',
                'is_staff': True,
                'is_superuser': True,
                'is_manager': True,
                'is_customer': False,
                'is_active': True,
            }
        )
        if created:
            manager.set_password("Admin123!")
            manager.save()
            self.stdout.write(self.style.SUCCESS("    + Manager yaratildi (+998901234567 / Admin123!)"))

        # 2. Customer User
        customer, created = User.objects.get_or_create(
            phone_number="+998919876543",
            defaults={
                'username': "+998919876543",  # AbstractUser DB constraint uchun
                'first_name': 'Zafarjon',
                'last_name': 'Mijoz',
                'is_staff': False,
                'is_superuser': False,
                'is_manager': False,
                'is_customer': True,
                'is_active': True,
            }
        )
        if created:
            customer.set_password("Customer123!")
            customer.save()
            self.stdout.write(self.style.SUCCESS("    + Customer yaratildi (+998919876543 / Customer123!)"))

        return manager, customer

    def _seed_catalog(self) -> dict[str, Product]:
        """Kategoriya va mahsulotlarni yaratish."""
        self.stdout.write("  -> Kategoriya va mahsulotlar yaratilmoqda...")

        # 1. Kategoriya: Pitsa
        cat_pizza, _ = Category.objects.get_or_create(
            name="Pitsa",
            defaults={'is_active': True}
        )
        
        prod_margarita, _ = Product.objects.get_or_create(
            name="Margarita Pitsa",
            category=cat_pizza,
            defaults={
                'price': Decimal('65000.00'),
                'is_available': True
            }
        )
        prod_pepperoni, _ = Product.objects.get_or_create(
            name="Pepperoni Pitsa",
            category=cat_pizza,
            defaults={
                'price': Decimal('75000.00'),
                'is_available': True
            }
        )

        # 2. Kategoriya: Ichimliklar
        cat_drinks, _ = Category.objects.get_or_create(
            name="Ichimliklar",
            defaults={'is_active': True}
        )

        prod_cola, _ = Product.objects.get_or_create(
            name="Coca-Cola 1.5L",
            category=cat_drinks,
            defaults={
                'price': Decimal('15000.00'),
                'is_available': True
            }
        )

        return {
            'margarita': prod_margarita,
            'pepperoni': prod_pepperoni,
            'cola': prod_cola
        }

    def _seed_orders(self, customer: Any, products: dict[str, Product]) -> None:
        """Namunaviy test buyurtmasini yaratish."""
        self.stdout.write("  -> Namunaviy buyurtma shakllantirilmoqda...")

        order, created = Order.objects.get_or_create(
            customer=customer,
            status=Order.StatusChoices.PREPARING,
            defaults={
                'delivery_phone_number': customer.phone_number,
                'delivery_address': "Toshkent sh., Yunusobod tumani, 4-mavze, 12-uy",
                'latitude': Decimal('41.311081'),
                'longitude': Decimal('69.240562'),
                'total_amount': Decimal('0.00')
            }
        )

        if created:
            # OrderItem 1: Pepperoni
            item1 = OrderItem.objects.create(
                order=order,
                product=products['pepperoni'],
                price=products['pepperoni'].price,
                quantity=1
            )
            # OrderItem 2: Cola
            item2 = OrderItem.objects.create(
                order=order,
                product=products['cola'],
                price=products['cola'].price,
                quantity=2
            )

            # Buyurtmaning umumiy summasini hisoblab yangilaymiz
            order.total_amount = item1.total_price + item2.total_price
            order.save()
            self.stdout.write(self.style.SUCCESS(f"    + Order #{order.id} yaratildi (Summa: {order.total_amount} so'm)"))