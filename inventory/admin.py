from django.contrib import admin
from .models import Products, Orders, Category, Vendors, Clients, Tickets

admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Category)
admin.site.register(Vendors)
admin.site.register(Clients)
admin.site.register(Tickets)
