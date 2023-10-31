import threading

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models.query import EmptyQuerySet
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic

from carts.utils import destroy_cart
from carts.utils import get_or_create_cart
from charges.models import Charge
from orders.decorators import validate_cart_and_order
from orders.mails import Mail
from orders.models import Order
from orders.utils import breadcrumb
from orders.utils import destroy_order
from orders.utils import get_or_create_order
from shipping_address.models import ShippingAddress

@login_required(login_url='login')
@validate_cart_and_order
def order(request, cart, order):
    
    return render(request, 'orders/order.html', {
        'cart' : cart,
        'order': order,
        'breadcrumb' : breadcrumb,
    })

@login_required(login_url='login')
@validate_cart_and_order
def address(request, cart, order):
    
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.has_shipping_addresses()
    return render(request, 'orders/address.html', {
        'cart' : cart,
        'order' : order,
        'shipping_address':shipping_address,
        'can_choose_address': can_choose_address,
        #address es tru para que quede activa
        'breadcrumb' : breadcrumb(address=True)
    })

@login_required(login_url='login')
def select_address(request):
    #obtenemos todas las direcciones del usuario autenticado
    shipping_addresses = request.user.addresses
    return render(request, 'orders/select_address.html', {
        'breadcrumb': breadcrumb(address=True),
        #pasamos la vista al template
        'shipping_addresses':shipping_addresses
    })

@login_required(login_url='login')
@validate_cart_and_order
def check_address(request, cart, order, pk):

    #obtenemos la dirección que el usuario selecciona
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    #validamos el usuario que es quien creo la dirección
    if request.user.id != shipping_address.user_id:
        #si es un usuario atacante
        return redirect('carts:cart')

    #actualizamos nuestra orden con el método update_shipping_address
    order.update_shipping_address(shipping_address)

    return redirect('orders:address')

@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart, order):

    #Es necesario que la orden de compra posea una dirección
    shipping_address = order.shipping_address
    if shipping_address is None:
        #lo retornamos al template de dirección
        return redirect('orders:address')
    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True, confirmation=True),
    })

@login_required(login_url='login')
@validate_cart_and_order
def cancel(request, cart, order):

    #si el usuario es diferente del dueño de la orden
    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()
    destroy_cart(request)
    destroy_order(request)

    messages.error(request, 'Orden Cancelada')
    return redirect('products:index')

@login_required(login_url='login')
@validate_cart_and_order
def complete(request, cart, order):

    #si el usuario es diferente del dueño de la orden
    if request.user.id != order.user_id:
        return redirect('carts:cart')

    charge = Charge.objects.create_charge(order)
    #si el cargo se genera de manera exitosa
    if charge:
        with transaction.atomic():
            #damos la orden por completada
            order.complete()
            #con el parámetro indicamos la función o el método
            #que se va a ejecutar en segundo plano
            thread = threading.Thread(target=Mail.send_complete_order, args=(
                order, request.user
            ))
            #ejecutamos el método start
            thread.start()
        
            destroy_cart(request)
            destroy_order(request)

            messages.success(request, 'Compra completada exitosamente')
    return redirect('products:index')

class OrderListView(LoginRequiredMixin, generic.ListView):
    #redireccionamos a los usuarios anonimos a la vista login
    login_url = 'login'
    template_name = 'orders/orders.html'

    def get_queryset(self):
        #por el momento retorna una lista vacia
        return self.request.user.orders_completed()