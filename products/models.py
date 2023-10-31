import uuid
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

#todas las clases que hereden de models.Model no es mas que la representación de una tabla en la BD
#y los atributos de la clase se convierten en las columnas de la tabla
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    #le indico que voy a tener un máximo de 8 digítos de los cuales 2 son decimales (123456.78)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    #no permitira almacenar valores nulos (null=False),
    #no permitira almacenar strings vacios (blank=False),
    #tendra solamente valores unicos (unique=True)
    slug = models.SlugField(null=False, blank=False, unique=True)
    #el upload_to es para indicar la ruta donde vamos a almacenar las imagenes
    image = models.ImageField(upload_to='products/', null=False, blank=True)
    #este atributo es para saber cuando es creado el producto
    created_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     #django nos provee de una funcion que genera Slugs a partir de un string la funcion es slugify()
    #     self.slug = slugify(self.title)
    #     #ejecutamos el metodo save de nuestra clase padre
    #     super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

def set_slug(sender, instance, *args, **kwargs):
    #preguntamos si i objeto posee un titulo y si mi objeto no posee un slug
    if instance.title and not instance.slug:
        slug = slugify(instance.title)
        #debemos validar que este slug no exista en la base de datos nos apoyamos con un ciclo while
        while Product.objects.filter(slug=slug).exists():
            #El slug lo generamos con un formato diferente
            #el primer valor seguira siendo su titulo y
            #luego una cadena de caracteres seudo aleatorio la cual nos apoyamos
            #de la libreria uuid, este tiene un metodo uuid4 el cual retorna un objeto
            #[:8] es para generar un strin de 8 caracteres
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )
        instance.slug = slug

#vamos a registrar el callback a nuestro modelo Product
#con esto le indicamos a django que antes que un objeto Product se almacene
#ejecute el callback set_slug
pre_save.connect(set_slug, sender=Product)
