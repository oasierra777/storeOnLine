from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path

from StoreOnLine import views

urlpatterns = [
    path('usuarios/login', views.login_view, name='login'),
    path('usuarios/logout', views.logout_view, name='logout'),
    path('usuarios/register', views.register, name='register'),
    path('admin/', admin.site.urls),
    #productos esta en espanol debido a que esta es a que se muestra al ususario
    path('productos/', include('products.urls', namespace='products')),
    path('carrito/', include('carts.urls', namespace='carts')),
    path('orden/', include('orders.urls', namespace='orders')),
    path('direcciones/', include('shipping_address.urls', namespace='shipping_address')),
    path('codigos/', include('promo_codes.urls', namespace='codes')),
    path('pagos/', include('billing_profiles.urls', namespace='billing_profiles')),
]

#esta condicion nos permite mostrar nuestras imagenes en el template
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
