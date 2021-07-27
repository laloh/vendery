from django.urls import path
from .views import *
app_name = 'panel'

urlpatterns = [
    path('', ViewAdminPanel.as_view(), name='view-admin-panel'),
    path('login', LoginPanel.as_view(), name='view-login-panel'),
    path('logout', LogoutPanel.as_view(), name='view-logout-panel'),
]
