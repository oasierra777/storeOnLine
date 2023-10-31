from stripeAPI import stripe

def create_charge(order):
	#Si la orden posee un método de pago y la orden posee un usuario
	#y nos aseguramos que el usuario posea un cliente en stripe 
	if order.billing_profile and order.user and order.user.customer_id:
		#generamos el cargo
		charge = stripe.Charge.create(
			#stripe maneja la cantidfad en centavos
			amount = int(order.totla) * 100,
			#moneda
			currency = 'USD',
			description = order.description,
			custumer = order.user.customer_id,
			#método de pago
			source = order.billing_profile.card_id,
			#esta atributo es información que queremos enviar 
			#deliberadamente al servidor de stripe 
			metadata = {
				'order_id':order.id
			}
		)

		return charge