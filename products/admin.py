from django.contrib import admin

from products.models import Product

class ProductAdmin(admin.ModelAdmin):
    #especificamos que campos queremos ver en el formulario y
    #nos apoyamos del atributo fiels que es un tupla
    fields = ('title', 'description', 'price', 'image')
    #list_display que es una tupla
    list_display = ('__str__', 'slug', 'created_at')

#pasamos como segundo argumento la clase
admin.site.register(Product, ProductAdmin)
