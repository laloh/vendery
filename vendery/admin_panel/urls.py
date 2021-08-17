from django.urls import path
from .views import *
app_name = 'panel'

urlpatterns = [
    path('', ViewAdminPanel.as_view(), name='view-admin-panel'),
    path('login', LoginPanel.as_view(), name='view-login-panel'),
    path('logout', LogoutPanel.as_view(), name='view-logout-panel'),
    path('categoria/', ViewCreateCategory.as_view(), name='view-create-category'),
    path('categorias/', ViewListCategory.as_view(), name='view-list-category'),
    path('categoria/<int:pk>/', ViewUpdateCategory.as_view(), name='view-update-category'),
    path('clientes/', ViewListClient.as_view(), name='view-list-client'),
    path('nuevo-cliente/', ViewCreateClient.as_view(), name='view-create-client'),
    path('cliente/<int:pk>/', ViewUpdateClient.as_view(), name='view-update-client'),
    path('productos/', ViewListProducts.as_view(), name='view-list-product'),
    path('nuevo-producto/', ViewCreateProducts.as_view(), name='view-create-product'),
    path('producto/<int:pk>/', ViewUpdateProducts.as_view(), name='view-update-product'),
    path('tickets/', ViewListTickets.as_view(), name='view-list-tickets'),
    path('nuevo-ticket/', ViewCreateTickets.as_view(), name='view-create-tickets'),
    path('ticket/<int:pk>/', ViewUpdateTickets.as_view(), name='view-update-tickets'),
    path('ventas/', ViewListSales.as_view(), name='view-list-sales'),
    path('nueva-venta/', ViewCreateSales.as_view(), name='view-create-sale'),
    path('venta/<int:pk>/', ViewUpdateSales.as_view(), name='view-update-sale'),
    path('provedores/', ViewListProvider.as_view(), name='view-list-provider'),
    path('nuevo-proveedor/', ViewCreateProvider.as_view(), name='view-create-provider'),
    path('proveedor/<int:pk>/', ViewUpdateProvider.as_view(), name='view-update-provider'),
    path('vendedores/', ViewListVendors.as_view(), name='view-list-vendors'),
    path('nuevo-vendedor/', ViewCreateVendors.as_view(), name='view-create-vendor'),
    path('vendedor/<int:pk>/', ViewUpdateVendors.as_view(), name='view-update-vendors'),
    path('talla/', ViewCreateProductSize.as_view(), name='view-create-product-size'),
    path('tallas/', ViewListProductSize.as_view(), name='view-list-product-size'),
]
