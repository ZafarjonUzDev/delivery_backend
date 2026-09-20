# from rest_framework import serializers
# from .models import Category, Product


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'slug', 'image')


# class ProductSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)

#     class Meta:
#         model = Product
#         fields = (
#             'id',
#             'category',
#             'name',
#             'slug',
#             'description',
#             'price',
#             'image',
#             'is_available',
#         )

from rest_framework import serializers
from .models import Category, Product


# ============================================================================
# CATEGORY SERIALIZERS
# ============================================================================

class CategoryListSerializer(serializers.ModelSerializer):
    """
    Kategoriyalar ro'yxati (List API) uchun yengil serializer.
    
    Bosh sahifada kategoriyalar tugmalarini tezkor chiqarish uchun xizmat qiladi.
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'is_active')


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Kategoriya tafsilotlari (Detail API) uchun serializer.
    
    Tanlangan kategoriya va uning ichidagi faol mahsulotlar ro'yxatini beradi.
    """
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'is_active', 'created_at', 'products')

    def get_products(self, obj):
        """Kategoriya ichidagi faol (is_available=True) mahsulotlarni yengil ko'rinishda qaytaradi."""
        active_products = obj.products.filter(is_available=True)
        return ProductListSerializer(active_products, many=True, context=self.context).data


# ============================================================================
# PRODUCT SERIALIZERS
# ============================================================================

class ProductListSerializer(serializers.ModelSerializer):
    """
    Mahsulotlar katalogi va ro'yxati (List API) uchun optimallashtirilgan yengil serializer.
    
    Mobil ilova va web frontendda cheksiz skroll (infinite scroll) paytida 
    tarmoq trafigini tejaydi va tezkor yuklanishni ta'minlaydi.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'category_name',
            'name',
            'price',
            'image',
            'is_available',
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Bitta mahsulot haqida to'liq ma'lumot (Detail API) beruvchi serializer.
    
    Mahsulot kartochkasi yoki modal oynasi ochilganda batafsil vaqt va 
    kategoriya ma'lumotlarini taqdim etadi.
    """
    category = CategoryListSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'name',
            'price',
            'image',
            'is_available',
            'created_at',
            'updated_at',
        )


# ============================================================================
# MANAGER CUD (CREATE / UPDATE / DELETE) SERIALIZERS
# ============================================================================

class ProductWriteSerializer(serializers.ModelSerializer):
    """
    Manager tomonidan mahsulot yaratish va tahrirlash uchun ishlatiladigan serializer.
    
    ForeignKey sifatida 'category' ID qiymatini qabul qiladi.
    """
    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'name',
            'price',
            'image',
            'is_available',
        )