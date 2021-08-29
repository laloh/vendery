from django.urls import path
from .views import *
app_name = 'landing'

urlpatterns = [
    path('', ViewLandingPage.as_view(), name='view-landing-page'),

]
