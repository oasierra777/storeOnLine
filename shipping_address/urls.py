from django.urls import path

from shipping_address import views

app_name = 'shipping_address'

urlpatterns = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_addresses'),
    path('nuevo', views.create, name='create'),
    path('editar/<int:pk>', views.ShippingAddressUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>', views.ShippingAddressDeleteView.as_view(), name='delete'),
    path('default/<int:pk>', views.default, name='default'),
]
