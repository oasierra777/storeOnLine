from django.urls import reverse

from orders.models import Order

def get_or_create_order(cart, request):

    order = cart.order

    #si la oreden no existe y si el usuario se encuentra autenticado
    #entonces creamos una orden asignando el carrito y el usuario
    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)
    #si la orden existe se actializa la sesion
    if order:
        request.session['order_id'] = order.id

    return order

def breadcrumb(products=True, address=False, payment=False, confirmation=False):
    #la funcion reverse recibe como argumento el nombre de una direccion retorna
    #la direccion persee, pro ejemplo reverse('orders:order') nos retorna /orden
    #y por el momento dejamos el reverse asi
    return[
        { 'title' : 'Productos', 'active' : products, 'url' : reverse('orders:order') },
        { 'title' : 'Direccion', 'active' : address, 'url' : reverse('orders:address') },
        { 'title' : 'Pago', 'active' : payment, 'url' : reverse('orders:order') },
        { 'title' : 'Confirmacion', 'active' : confirmation, 'url' : reverse('orders:confirm') }
    ]

def destroy_order(request):
    #El None nos permite destruir una sesión 
    request.session['order_id'] = None