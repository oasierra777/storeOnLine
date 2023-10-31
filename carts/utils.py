from carts.models import Cart

def get_or_create_cart(request):
    #Si el usuario se encuentra autenticado obtenemos el usuario actual
    #en caso contrario None por la relacion del modelo
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id')

    cart = Cart.objects.filter(cart_id=cart_id).first()
    if cart is None:
        cart = Cart.objects.create(user=user)
    #El usuario existe y el carrito no posee un usuario
    if user and cart.user is None:
        cart.user = user
        cart.save()

    #Actualizamos la session, la sesion esta actualizando el id del carrito
    request.session['cart_id'] = cart.cart_id
    return cart

def destroy_cart(request):
    #El None nos permite destruir una sesión 
    request.session['cart_id'] = None