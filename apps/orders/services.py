from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.catalog.models import Product
from .models import Order, OrderItem


def create_order(*, customer, delivery_phone_number: str, delivery_address: str, 
                 items_data: list[dict], latitude=None, longitude=None) -> Order:
    """
    Buyurtma yaratish bo'yicha asosiy atomik servis (Business Logic Service).
    
    Enterprise Standard:
    - @transaction.atomic: Barcha amallar bitta tranzaksiya ichida bajariladi. 
      Biror xatolik bo'lsa, butun buyurtma va uning item'lari rollback qilinadi.
    - select_for_update(): Race condition (bir vaqtda bir nechta so'rov kelishi) 
      xavfini oldini olish uchun mahsulot qatorlarini lock qiladi.
    - Price Snapshotting: Mahsulotning AYNAN SOTIB OLINGAN PAYTDAGI narxini fiksatsiya qiladi.
    """
    
    with transaction.atomic():
        # 1. Asosiy Order obyektini 0 summa bilan yaratamiz
        order = Order.objects.create(
            customer=customer,
            delivery_phone_number=delivery_phone_number,
            delivery_address=delivery_address,
            latitude=latitude,
            longitude=longitude,
            total_amount=Decimal('0.00')
        )

        total_amount = Decimal('0.00')
        order_items_to_create = []

        # 2. Barcha mahsulot ID'larini yig'ib olamiz
        product_ids = [item['product_id'] for item in items_data]

        # 3. High-Load Protection: Mahsulotlarni DB darajasida qulflaymiz (SELECT ... FOR UPDATE)
        products_map = {
            product.id: product 
            for product in Product.objects.select_for_update().filter(id__in=product_ids, is_available=True)
        }

        # 4. OrderItem'larni shakllantiramiz hamda narxlarni snapshot qilamiz
        for item in items_data:
            product_id = item['product_id']
            quantity = item['quantity']

            product = products_map.get(product_id)
            if not product:
                raise ValidationError(
                    f"ID: {product_id} bo'lgan mahsulot bazada topilmadi yoki hozirda sotuvda yo'q."
                )

            # Snapshotted Price (Joriy narxni saqlaymiz)
            unit_price = product.price
            item_total = unit_price * quantity
            total_amount += item_total

            order_items_to_create.append(
                OrderItem(
                    order=order,
                    product=product,
                    price=unit_price,
                    quantity=quantity
                )
            )

        # 5. Barcha OrderItem'larni bazaga 1 ta SQL so'rov bilan ommaviy saqlaymiz (Bulk Create)
        OrderItem.objects.bulk_create(order_items_to_create)

        # 6. Yakuniy umumiy summani buyurtmaga yozib saqlaymiz
        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])

        return order