from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from carts.models import Cart
from carts.models import CartProducts
from carts.utils import get_or_create_cart
from products.models import Product

def cart(request):
    cart = get_or_create_cart(request)
    return render(request, 'carts/carts.html', {'cart':cart})

def add(request):
    #obtenemos el carrito de compras
    cart = get_or_create_cart(request)
    #luego obtenemos el producto
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    #esta cantidad la traemos del formulario desde el input cuyo nombre es quantity
    #si la llave no existe por defecto colocamos 1
    quantity = int(request.POST.get('quantity', 1))
    #agregamos al carrito de compras
    # cart.products.add(product, through_defaults={
    #     'quantity':quantity
    # })
    cart_product = CartProducts.objects.create_or_update_quantity(cart=cart,
                                                                product=product,
                                                                quantity=quantity)

    return render(request, 'carts/add.html', {
        'quantity':quantity,
        'cart_product':cart_product,
        'product' : product
    })

def remove(request):
    cart = get_or_create_cart(request)
    #nos permite obtener un objeto a partir de una condicion
    product = get_object_or_404(Product, pk = request.POST.get('product_id'))

    cart.products.remove(product)

    return redirect('carts:carts')
