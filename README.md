# Universal Multi-Branch Delivery Service API

Universal Multi-Branch Delivery API Backend — bu restoranlar, kafelar va chakana savdo do'konlari uchun mo'ljallangan, yuqori unumdorlikka ega, Clean Architecture hamda DDD (Domain-Driven Design) tamoyillari asosida qurilgan enterprise RESTful backend xizmatidir.

## 🚀 Texnologik Stak
- **Core**: Python 3.12, Django 5.x, Django REST Framework
- **Architecture**: Domain-Driven Design (DDD), Clean Architecture, Layered Services
- **Database**: PostgreSQL (3NF Normalization, Indexing, Atomic Transactions)
- **Authentication**: Custom User Model (Phone Authentication), JWT (SimpleJWT), Role-Based Access Control (RBAC)
- **Documentation**: OpenAPI 3.0, Swagger UI (`drf-spectacular`)
- **DevOps**: Docker, Docker Compose

## 🛠️ Arxitektura Xususiyatlari
- **Concurrency & Financial Safety**: Buyurtma yaratishda race condition'larning oldini olish uchun `@transaction.atomic` va `select_for_update()` qo'llanilgan.
- **Price Snapshotting**: Buyurtma paytidagi mahsulot narxi `OrderItem` modelida saqlanadi, bu esa kelajakda mahsulot narxi o'zgarganda moliyaviy hisobotlar buzilmasligini ta'minlaydi.
- **Query Optimization**: N+1 so'rovlar muammosini oldini olish uchun `select_related` va `prefetch_related` so'rovlaridan foydalanilgan.
- **Payload Optimization**: Barcha ilovalarda yengil `ListSerializer` va batafsil `DetailSerializer` pattern'lari qo'llanilgan.

## ⚙️ Loyihani Mahalliy Muhitda Ishga Tushirish

1. **Repozitoriyani klonlash:**
   ```bash
   git clone [https://github.com/ZafarjonUzDev/delivery_backend.git](https://github.com/ZafarjonUzDev/delivery_backend.git)
   cd delivery_backend