from django.contrib import admin

from demo.forms import OrderForm
from demo.models import *


class ItemInstanceInline(admin.TabularInline):
    model = Goods


class OrdersAdmin(admin.ModelAdmin):
    form = OrderForm
    list_filter = ('role',)
    list_display = ('date', 'user', 'count_product')
    fields = ['role', 'reason']
    inlines = [ItemInstanceInline]


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Goods)
admin.site.register(Basket)
admin.site.register(Orders, OrdersAdmin)
