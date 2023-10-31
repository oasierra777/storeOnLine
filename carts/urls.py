from django.urls import path

from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='carts'),
    path('agregar', views.add, name='add'),
    path('eliminar', views.remove, name='remove'),
]
