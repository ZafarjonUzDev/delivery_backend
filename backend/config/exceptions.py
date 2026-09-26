import logging
from typing import Any, Dict, Optional

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

# Markazlashgan ilova loggeri
logger = logging.getLogger('django')


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[Response]:
    """
    Django REST Framework uchun global xatoliklarni ushlash va standartlashtirish funksiyasi.

    Ushbu handler loyihadagi barcha API xatoliklarini yagona va unifikatsiyalangan
    JSON strukturasiga keltirish uchun xizmat qiladi. Tizimda kutilmagan va ushlanmagan
    server xatoliklarini (500 Internal Server Error) ushlab, ularni full stack trace
    ko'rinishida logs/errors.log fayliga yozadi hamda foydalanuvchiga xavfsiz va
    tushunarli xabar qaytaradi.

    Standartlashtirilgan Xatolik JSON Formati:
    {
        "status": "error",
        "status_code": <int>,
        "errors": <dict_yoki_list>
    }

    Parametrlar:
        exc (Exception): Yuzaga kelgan xatolik obyekti.
        context (dict): Xatolik yuz bergan so'rov (request) va view haqida qo'shimcha kontekst.

    Qaytaradi:
        Optional[Response]: Formatlangan va unifikatsiyalangan DRF Response obyekti.
    """
    # DRF ning standart exception handler'ini chaqirib, mavjud response'ni olamiz
    response = exception_handler(exc, context)

    if response is not None:
        # Mijoz tomonidan yuzaga kelgan (4xx) xatoliklarni yagona formatga keltiramiz
        custom_response_data: Dict[str, Any] = {
            'status': 'error',
            'status_code': response.status_code,
            'errors': response.data
        }
        response.data = custom_response_data
    else:
        # Tizimda ushlanmagan server xatoliklarini (500) tutamiz va logga yozamiz
        request = context.get('request')
        path: str = request.path if request else 'Noma\'lum yo\'l'
        method: str = request.method if request else 'Noma\'lum metod'

        # Xatolik tafsilotlarini logs/errors.log fayliga yozish
        logger.error(
            f"Ushlanmagan ilova xatoligi: {str(exc)} | Metod: {method} | Yo'l: {path}",
            exc_info=True
        )

        # Xavfsizlik nuqtai nazaridan koddagi ichki xatoliklarni mijozga ko'rsatmasdan,
        # standart 500 JSON javobini qaytaramiz
        response = Response(
            {
                'status': 'error',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'errors': {
                    'detail': 'Ichki server xatoligi yuz berdi. Iltimos, birozdan so\'ng qayta urinib ko\'ring.'
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response