from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def create(request):
	#El formulario ha realizado el submit
	if request.method == 'POST':
		#el formulario nos envía el token para generar una nueva tarjeta
		if request.POST.get('sripeToken'):
			#antes de crear la tarjeta es necesario validar si el usuario
			#posee o no un cliente en stripe en caso de no poseer es necesario
			#dar de alta o crear uno nuevo, inocamos el método que creamos antes
			if not request.user.has_customer():
				#en caso no posea un cliente
				request.user.create_customer_id()
				
	return render(request, 'billing_profiles/create.html', {
		'stripe_public_key':settings.STRIPE_PUBLIC_KEY
	})