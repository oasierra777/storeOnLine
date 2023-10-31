from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('search', views.ProductSearchView.as_view(), name='search'),
    #Estamos indicando que vamos abuscar porelatributo slug
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product'),
]
