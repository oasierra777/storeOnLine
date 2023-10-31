import string
import random

from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

class PromoCodeManager(models.Manager):

	def get_valid(self, code):
		#conocemos la fecha actual
		now = timezone.now()
		#condiciones que debemos implementar si el código es válido
		return self.filter(code=code).filter(used=False).filter(valid_from__lte=now).filter(valid_to__gte=now).first()

class PromoCode(models.Model):
	code = models.CharField(max_length=50, unique=True)
	discount = models.FloatField(default=0.0)
	valid_from = models.DateTimeField()
	valid_to = models.DateTimeField()
	used = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	#extendemos el objeto y de esta forma hará uso del método get_valid 
	objects = PromoCodeManager()

	def __str__(self):
		return self.code

	def use(self):
		#actualiza el atributo used para saber si el código ha sido utilizado
		self.used = True
		self.save()


def set_code(sender, instance, *args, **kwargs):
	#si existe un código promocienale entonces terminamos la función 
	if instance.code:
		return

	#definimos nuestra lista de caracteres
	chars = string.ascii_uppercase + string.digits
	#en caso contrario asignamos un código
	instance.code = ''.join(random.choice(chars) for _ in range(10))


pre_save.connect(set_code, sender=PromoCode)