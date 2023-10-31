#esta clase enviamos mensajes del servidor al cliente
from django.contrib import messages
#nos permite autenticar a un usuario y saber si está en la base de datos
from django.contrib.auth import authenticate
#es la encargade de inicar sesión
from django.contrib.auth import login
#es la encargade de cerrar sesión
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
#podemos dar de alta nuevos usuarios
#from django.contrib.auth.models import User
#esta clase nos permite responde a la petición de un cliente mediante un template rendirizado
from django.shortcuts import render
from django.shortcuts import redirect

from products.models import Product
from StoreOnLine.forms import RegisterForm
from users.models import User

def index(request):
    products = Product.objects.all().order_by('-id')
    #render recibe de forma obligatoria 3 argumentos, el primero es la petición,
    #el segundo es un string que es el nombre del template que necesitamos utilizar
    #y el tercer argumento es un diccionario que hace referenca a un contexto
    #con el contexto puedo pasar valores de nuestra vista a nuestro template
    context = {
        'title': 'Productos',
        'message': 'Listado de Productos',
        'products': products,
    }
    return render(request, 'index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    #request obtiene toda la información relacionada a la petición
    if request.method == 'POST':
        #el atributo POST no es más que un diccionario por lo tanto podemos utilizar su método get
        username = request.POST.get('username')
        password = request.POST.get('password')
        #la función no retorna un objeto de tipo user y si no encuentra el ususario
        #con esa contrasena nos retorna None
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            #si la petiion posee el parametro next en la url
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])
            #La función recibe un parámetro string el cual es la dirección a donde vamos a dirigir
            return redirect('products:index')
        else:
            messages.error(request, 'Usuario o contrasena NO validos')
    return render(request, 'users/login.html', {})

def logout_view(request):
    #el objeto request ya posee la sesión
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    #si es POST genera un formulario con los datos que el cliente le está enviando
    #si es None genera un formulario vacio
    form = RegisterForm(request.POST or None)
    #validamos que los datos sean validas
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            #Generamos la sesion
            login(request, user)
            messages.success(request, 'Usuario creado de manera exitosa')
            return redirect('index')
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

    #esto es lo que estaba antes
    # if request.method == 'POST' and form.is_valid():
    #     #form.cleaned_data es un diccionario y podemosutilizar el método get
    #     username = form.cleaned_data.get('username')
    #     email = form.cleaned_data.get('email')
    #     password = form.cleaned_data.get('password')
    #     #create_user nos retorna un objeto de tipo user si fue posible crearlo
    #     user = User.objects.create_user(username, email, password)
    #     if user:
    #         #Generamos la sesion
    #         login(request, user)
    #         messages.success(request, 'Usuario creado de manera exitosa')
    #         return redirect('index')
    # context = {
    #     'form': form
    # }
    # return render(request, 'users/register.html', context)
