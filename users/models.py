from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User

from orders.common import OrderStatus
from stripeAPI.customer import create_customer

class User(AbstractUser):

    customer_id = models.CharField(max_length=100, blank=True, null=True)

    def get_full_name(self):
        return '{} {}'.formt(self.first_name, self.last_name)

    @property
    def shipping_address(self):
        #obtenemos la direccion principal del usuario
        return self.shippingaddress_set.filter(default=True).first()

    @property
    def description(self):
        #podemos colocar la descripción que se crea conveniente
        return 'Descripción para el usuario {}'.format(self.username)

    def has_customer(self):
        #si el usuario posee un cliente en stripe
        return self.customer_id is not None

    def create_customer_id(self):
        #realizamos siempre y cuando el usuario
        #no posea un customer_id
        if not self.has_customer():
            #el parámetro es de tipo user pero como
            #estamos en el modelo de user pasa self
            customer = create_customer(self)
            #id es un atributo que el servidor nos responde
            self.customer_id = customer.id
            #actualizamos el registro
            self.save()

    def has_shipping_address(self):
        #con este metodo vamos a conocer si el usuario posee o no una direccon principal
        return self.shipping_address is not None

    def orders_completed(self):
        #mostramos la ordenes de forma desendente con respecto a su creación
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')

    def has_shipping_addresses(self):
        return self.shippingaddress_set.exists()

    @property
    def addresses(self):
        return self.shippingaddress_set.all()

class Customer(User):
    class Meta:
        proxy = True

    def get_products(self):
        #retorna todos los productos adquridos por el usuario
        return []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
