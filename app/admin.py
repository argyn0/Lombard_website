from django.contrib import admin
from .models import CustomUser, GoldCost, Category, Product, BailTicket

admin.site.register(CustomUser)
admin.site.register(GoldCost)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(BailTicket)