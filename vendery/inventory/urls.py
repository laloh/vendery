from django.urls import path
from .views import *

app_name = 'inventory'

urlpatterns = [
    path('', ViewInventory.as_view(), name='view-inventory'),
    path('login', Login.as_view(), name='view-login'),
    path('logout', Logout.as_view(), name='view-logout'),
]

