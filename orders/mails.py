from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse #retorna un string

class Mail:

	@staticmethod
	def get_absolute_url(url):
		if settings.DEBUG: #En modo desarrollo
			return 'http://localhost:8000{}'.format(
				reverse(url)
			)

	@staticmethod
	def send_complete_order(order, user):
		subject = 'Tú pedido ha sido enviado'
		template = get_template('orders/mails/complete.html')
		content = template.render({
			'user':user,
			'order':order,
			'next_url':Mail.get_absolute_url('orders:completeds')
		})

		message = EmailMultiAlternatives(subject,
										'Mensaje importante',
										settings.EMAIL_HOST_USER,
										[user.email])
		#Asignamos un contenido text/html es el formato
		message.attach_alternative(content, 'text/html')
		#enviamos el mensaje
		message.send()