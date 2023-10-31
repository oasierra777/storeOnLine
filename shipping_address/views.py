from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.views import generic
from django.urls import reverse_lazy

from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order
from shipping_address.forms import ShippingAddressForm
from shipping_address.models import ShippingAddress

class ShippingAddressListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        #obtenemos todas las direcciones del ususario autenticado y las ordenamos
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Direccion actualizada Exitosamente'

    def get_success_url(self):
        return reverse('shipping_address:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        #si el usuario que realizo la peticion no le corresponde esta direccion
        #la direccion la obtenemos con get_object entonces lo redireccionamos a carrito de compras
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAddressDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy('shipping_address:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('shipping_address:shipping_addresses')
        #solo los usuarios duenos de esa direccion pueden eliminarla
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        #si el objeto shippingaddress posee ordenes
        if self.get_object().has_orders():
            return redirect('shipping_address:shipping_addresses')
        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='login')
def create(request):
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        #para  colocar por defaul la primera direccion que registra el ususario.
        shipping_address.default = not request.user.has_shipping_address()
        shipping_address.save()

        #si la petición posee el parámetro next
        if request.GET.get('next'):
            if request.GET['next'] == reverse('orders:address'):
                cart = get_or_create_cart(request)
                order = get_or_create_order(cart, request)

                order.update_shipping_address(shipping_address)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Direccion Creada Exitosamente')
        return redirect('shipping_address:shipping_addresses')


    return render(request, 'shipping_addresses/create.html', {'form':form})

@login_required(login_url='login')
def default(request, pk):
    #nos permite obtener un objeto dela base de datos a partir de una condicion
    #si el onjeto no  existe entonces envia al cliente el error 404
    #la base de datos es ShippingAddress y el filto la pk
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)
    #validamos que el usuario que creo la direccion sea el unico que pueda editarla
    #si es otro usuario que lo redirija al carrito de compra
    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    if request.user.has_shipping_address():
        #obtener la antigua direccion principal y colocar default=False
        request.user.shipping_address.update_default()

    #creamos el metodo en el modelo ShippingAddress
    shipping_address.update_default(True)

    return redirect('shipping_address:shipping_addresses')
