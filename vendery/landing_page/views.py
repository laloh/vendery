from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, ListView
from vendery.inventory.models import Products
from xhtml2pdf import pisa


class ViewLandingPage(ListView):
    """ Landing"""
    template_name = "landing/index.html"
    context_object_name = "products"
    model = Products


def render_pdf_view_products(request, *args, **kwargs):
    products = Products.objects.all().order_by('name')
    template_path = 'landing/products_pdf.html'
    host = request.get_host()
    tenant = f"{request.tenant.schema_name}/img/"
    context = {'products': products,
               'host': host,
               'tenant': tenant}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
