# ==========================================
# Production-Ready Nginx Frontend Engine
# ==========================================
FROM nginx:1.26-alpine AS runner

# Nginx uchun kesh va temp kataloglar huquqlarini to'g'rilash
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx

# Nginx konfiguratsiyasini o'rnatish
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Statik web resurslarni ko'chirish va huquqlarni berish
COPY --chown=nginx:nginx . /usr/share/nginx/html

# Xavfsizlik bo'yicha Nginx'ni non-root (nginx) foydalanuvchi sifatida ishga tushirish
USER nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --spiders http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]