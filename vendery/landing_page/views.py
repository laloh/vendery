from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from vendery.inventory.models import Products


class ViewLandingPage(ListView):
    """ Landing"""
    template_name = "landing/index.html"
    context_object_name = "products"
    model = Products

