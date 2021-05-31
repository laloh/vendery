from django.views.generic import TemplateView


class ViewInventory(TemplateView):
    """ Inventory index"""
    template_name = "index.html"

