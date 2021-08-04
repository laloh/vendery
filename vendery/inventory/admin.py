from django.contrib import admin
from .models import Products, Orders, Category, Vendors, Clients, Tickets, TemporaryOrders, Provider
from django.contrib.auth.admin import UserAdmin

admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Category)
admin.site.register(Vendors)
admin.site.register(Clients)
admin.site.register(Tickets)
admin.site.register(Provider)
admin.site.register(TemporaryOrders)
