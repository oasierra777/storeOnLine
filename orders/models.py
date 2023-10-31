import decimal
import uuid
from django.db import models
from django.db.models.signals import pre_save

from billing_profiles.models import BillingProfile
from carts.models import Cart
from orders.common import OrderStatus
from orders.common import choices
from promo_codes.models import PromoCode
from shipping_address.models import ShippingAddress
from users.models import User

class Order(models.Model):
    order_id = models.CharField(max_length=100, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=choices, default=OrderStatus.CREATED)#Enum
    shipping_total = models.DecimalField(default=5, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.CASCADE)
    promo_code = models.OneToOneField(PromoCode, null=True, blank=True, on_delete=models.CASCADE)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id

    def apply_promo_code(self, promo_code):
        #la orden no posee un código promocional
        if self.promo_code is None:  
            #asignamos el código promocional a la orden          
            self.promo_code = promo_code
            self.save()

            #actualizamos el total
            self.update_total()
            promo_code.use()

    def get_or_set_shipping_address(self):
        #si la orden posee una direccion de envio entonces la retornamos
        if self.shipping_address:
            return self.shipping_address
        #sino obtiene la direccion del usuario
        shipping_address = self.user.shipping_address
        #si posee una direccion la actiualizamos
        if shipping_address:
            self.update_shipping_address(shipping_address)
        return shipping_address

    def update_shipping_address(self, shipping_address):
        self.shipping_address = shipping_address
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELED
        self.save()  

    def complete(self):
        self.status = OrderStatus.COMPLETED
        self.save()
        
    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_discount(self):
        #si la orden posee un código promocional
        if self.promo_code:
            return self.promo_code.discount 

        #la orden no posee código promocional
        return 0

    def get_total(self):
        #total del carrito mas el costo de envio
        return self.cart.total + self.shipping_total - decimal.Decimal(self.get_discount())

    @property
    def description(self):
        return 'Comprar por ({}) productos '.format(
            self.cart.products.count()
        )

def set_order_id(sender, instance, *args, **kwargs):
    #si la orden no posee un order_id se la asignamos
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(set_order_id, sender=Order)
#antes que un objeto de tipo order se almacene se ejecuta el callback set_total
pre_save.connect(set_total,  sender=Order)
