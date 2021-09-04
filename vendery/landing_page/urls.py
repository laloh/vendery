from django.urls import path
from .views import *
app_name = 'landing'

urlpatterns = [
    path('', ViewLandingPage.as_view(), name='view-landing-page'),
    path('pdf/', render_pdf_view_products, name='view-landing-pdf'),

]
