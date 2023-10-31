from django.http import JsonResponse
from django.shortcuts import render

from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order
from promo_codes.models import PromoCode

def validate(request):
	#obtenemos el carrito y la orden
	cart = get_or_create_cart(request)
	order = get_or_create_order(cart, request)
	#recuperamos el código que el usuario nos envía
	code = request.GET.get('code')
	#obtenemos el promo_code llamamos el nuevo método
	promo_code = PromoCode.objects.get_valid(code)

	#no existe un objeto promo_code a partir del código
	if promo_code is None:
		return JsonResponse({
				'status':False
			}, status=404)#recurso no encontrado

	order.apply_promo_code(promo_code)

	#si existe un código 
	return JsonResponse({
		'status' : True,
		'code': promo_code.code,
		'discount' : promo_code.discount,
		'total' : order.total
	})

