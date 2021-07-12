from django.contrib import admin
from .models import Products, Orders, Category, Vendors, Clients, Tickets, TemporaryOrders
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Category)
admin.site.register(Vendors)
admin.site.register(Clients)
admin.site.register(Tickets)
admin.site.register(TemporaryOrders)
admin.site.register(User, UserAdmin)
