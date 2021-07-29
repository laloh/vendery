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

]
