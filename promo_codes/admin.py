from django.contrib import admin

from promo_codes.models import PromoCode

class PromoCodeAdmin(admin.ModelAdmin):
	exclude = ['code']

admin.site.register(PromoCode, PromoCodeAdmin)
