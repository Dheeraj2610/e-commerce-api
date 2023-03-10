from django.contrib import admin
from core.models import registration,Category,Product,Order,CartItem,Contact
# Register your models here.
admin.site.register(registration)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Contact)