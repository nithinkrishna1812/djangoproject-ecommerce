from django.contrib import admin
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'catogery', 'price', 'active']
    list_editable = ['catogery', 'active']

    class Meta:
        model = Product


admin.site.register(Catogery)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
