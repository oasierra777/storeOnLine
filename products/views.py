from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from products.models import Product

class ProductListView(generic.ListView):
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('-id')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        #este método se encarga de pasar el contexto de la clase a el template
        context = super().get_context_data(**kwargs)
        #obtenemos el contexto de la clase padre
        context['message'] = 'Listado de productos'
        #generar una nueva llave
        context['products'] = context['object_list']
        #o tambien se puede context['products'] = context['product_list']
        return context

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print(context)
        return context

class ProductSearchView(generic.ListView):
    template_name = 'search.html'

    def get_queryset(self):
        #como no está el atributo arribita entonces retornamos el queryset y hacemos
        #la consulta directamente, comparamos title con self.query que es el método que
        #hacemos abajo debido a que la consulta se hace por método get desde el html
        #en title le adicionamos __icontains
        #traducido a sql=SELECT * FROM products WHERE title like %valor%
        #la i indica que no es sencible a mayusculas y minusculas
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)

    def  query(self):
        #q es el parámetro que recibimos de la consulta get desde el html
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()
        return context
