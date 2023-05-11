from django.contrib import admin

from .models import Basket, Like

admin.site.register(Like, admin.ModelAdmin)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('product', 'id_user', 'count', 'buy_now')
