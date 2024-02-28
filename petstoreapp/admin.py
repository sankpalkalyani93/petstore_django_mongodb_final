from django.contrib import admin
from .models import Pet, Product, Cart, CartItem, CustomUser

# Register your models here.
admin.site.register(Pet)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CustomUser)