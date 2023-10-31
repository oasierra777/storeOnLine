from django.urls import path

from promo_codes import views

app_name = 'promo_codes'

urlpatterns = [
	path('validar', views.validate, name='validar')
]