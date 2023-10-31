from django.db import models

from users.models import User

class BillingProfile(models.Model):
	#un usuario puede tener muchos métodos de pago
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=50, null=False, blank=False)
	card_id = models.CharField(max_length=50, null=False, blank=False)
	last4 = models.CharField(max_length=4, null=False, blank=False)
	brand = models.CharField(max_length=10, null=False, blank=False)
	default = models.BooleanField(default=False)
	creted_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.card_id
