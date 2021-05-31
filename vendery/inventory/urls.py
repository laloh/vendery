from django.urls import path
from .views import *

app_name = 'inventory'

urlpatterns = [
    path('', ViewInventory.as_view(), name='view-inventory'),
]
