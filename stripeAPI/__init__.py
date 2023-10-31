import stripe
from django.conf import settings

#esta líne es obligatoria sin esta línea de 
#código no podemos acceder a la API
stripe.api_key =settings.STRIPE_PRIVATE_KEY