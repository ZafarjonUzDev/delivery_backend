# from django.db import transaction
# from rest_framework import serializers

# from apps.catalog.models import Product
# from .models import Order, OrderItem


# class OrderItemCreateSerializer(serializers.Serializer):
#     product_id = serializers.IntegerField()
#     quantity = serializers.IntegerField(min_value=1)


# class OrderItemSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(source='product.name', read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ('id', 'product', 'product_name', 'price', 'quantity', 'get_cost')


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Order
#         fields = (
#             'id',
#             'user',
#             'delivery_address',
#             'phone_number',
#             'total_amount',
#             'status',
#             'created_at',
#             'items',
#         )
#         read_only_fields = ('user', 'total_amount', 'status', 'created_at')


# class OrderCreateSerializer(serializers.ModelSerializer):
#     """
#     Buyurtma yaratish uchun maxsus serializer.
#     Atomik tranzaksiya va narxlarni fiksatsiya qilish mantig'ini o'z ichiga oladi.
#     """

#     items = OrderItemCreateSerializer(many=True, write_only=True)

#     class Meta:
#         model = Order
#         fields = ('id', 'delivery_address', 'phone_number', 'items')

#     def validate_items(self, value):
#         if not value:
#             raise serializers.ValidationError("Buyurtmada kamida bitta mahsulot bo'lishi kerak.")
#         return value

#     @transaction.atomic
#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         user = self.context['request'].user

#         # 1. Buyurtma asosiy obyektini yaratamiz
#         order = Order.objects.create(
#             user=user,
#             delivery_address=validated_data.get('delivery_address'),
#             phone_number=validated_data.get('phone_number'),
#             total_amount=0,  # Boshlang'ich 0, pastda hisoblanadi
#         )

#         total_price = 0

#         # 2. Har bir mahsulotni fiksatsiya qilingan joriy narxi bilan saqlaymiz
#         for item in items_data:
#             product_id = item['product_id']
#             quantity = item['quantity']

#             try:
#                 product = Product.objects.select_for_update().get(id=product_id, is_available=True)
#             except Product.DoesNotExist:
#                 raise serializers.ValidationError(
#                     f"ID: {product_id} bo'lgan mahsulot topilmadi yoki sotuvda yo'q."
#                 )

#             # Mahsulotning AYNAN HRGI JORIY NARXINI fiksatsiya qilamiz
#             current_price = product.price
#             item_total = current_price * quantity
#             total_price += item_total

#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 price=current_price,  # Snapshotted price
#                 quantity=quantity,
#             )

#         # 3. Yakuniy umumiy summani buyurtmaga yozamiz
#         order.total_amount = total_price
#         order.save()

#         return order


from rest_framework import serializers
from apps.catalog.models import Product
from .models import Order, OrderItem


# ============================================================================
# ORDER ITEM SERIALIZERS
# ============================================================================

class OrderItemCreateSerializer(serializers.Serializer):
    """
    Buyurtma yaratish paytida frontend yuboradigan yengil input payload.
    
    Format: [{"product_id": 1, "quantity": 2}, ...]
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """
    Buyurtma chekida har bir mahsulot va uning fiksatsiyalangan narxini aks ettiruvchi serializer.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'product_image', 'price', 'quantity', 'total_price')


# ============================================================================
# ORDER SERIALIZERS (LIST / DETAIL / CREATE)
# ============================================================================

class OrderListSerializer(serializers.ModelSerializer):
    """
    Mijozning buyurtmalar tarixi va ro'yxati (List API) uchun yengil serializer.
    
    Har bir buyurtmaning faqat asosiy statik ma'lumotlarini qaytarib, tarmoq trafigini tejaydi.
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'delivery_phone_number',
            'total_amount',
            'status',
            'status_display',
            'delivery_address',
            'created_at',
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Muayyan buyurtma cheki va uning barcha mahsulotlari (Detail API) uchun to'liq serializer.
    """
    items = OrderItemDetailSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'delivery_phone_number',
            'total_amount',
            'status',
            'status_display',
            'delivery_address',
            'latitude',
            'longitude',
            'created_at',
            'updated_at',
            'items',
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Buyurtma yaratish uchun input validatsiya serializer'i.
    """
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'delivery_phone_number',
            'delivery_address',
            'latitude',
            'longitude',
            'items',
        )

    def validate_items(self, value):
        """Buyurtma tarkibida kamida bitta mahsulot borligini va ID'lar to'g'riligini tekshiradi."""
        if not value:
            raise serializers.ValidationError("Buyurtmada kamida bitta mahsulot bo'lishi kerak.")
        
        # Mahsulot ID'lari takrorlanmaganini tekshirish
        product_ids = [item['product_id'] for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Bir xil mahsulot buyurtma ro'yxatida takrorlanmasligi kerak.")

        # Bazada mavjud va sotuvda borligini tekshirish
        existing_products = Product.objects.filter(id__in=product_ids, is_available=True).values_list('id', flat=True)
        missing_products = set(product_ids) - set(existing_products)
        if missing_products:
            raise serializers.ValidationError(f"Quyidagi ID'li mahsulotlar topilmadi yoki sotuvda yo'q: {list(missing_products)}")

        return value