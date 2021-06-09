from django.urls import path
from .views import *

app_name = 'inventory'

urlpatterns = [
    path('', ViewInventory.as_view(), name='view-inventory'),
    path('login', Login.as_view(), name='view-login'),
    path('logout', Logout.as_view(), name='view-logout'),
    path('mis-ventas', ViewSales.as_view(), name='view-sales'),
    path('venta', ViewSalesData.as_view(), name='view-sales-data'),
    path('nota-remision', ViewNote.as_view(), name='view-note'),
    path('inventario', ViewInventoryAll.as_view(), name='view-inventory-all'),
    path('clientes', ViewCustomers.as_view(), name='view-customers'),
]

