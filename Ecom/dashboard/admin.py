from django.contrib import admin
from .models import CustomUser, Product, Cart, RegisterSeller, ProductImages,Order,MiniOrder

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(RegisterSeller)
admin.site.register(ProductImages)
admin.site.register(Order)
admin.site.register(MiniOrder)