from django.contrib import admin
from .models import Products, Category, Vendors, Clients, Provider, Expenses
from django.contrib.auth.admin import UserAdmin

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Vendors)
admin.site.register(Clients)
admin.site.register(Provider)
admin.site.register(Expenses)
