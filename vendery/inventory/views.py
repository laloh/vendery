import os
import json
import time

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
from twilio.rest import Client
from datetime import date
from datetime import datetime



from .forms import AuthenticationFormUser, ClientForm, OrdersForm, ProductsForm, TicketsForm
from .models import Vendors, Tickets, Clients, Products, Orders


class Login(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationFormUser
    success_url = reverse_lazy('inventory:view-inventory')
    redirect_authenticated_user = True

    def get_success_url(self):
        url = super().get_redirect_url()
        return url or self.success_url


class Logout(LogoutView):
    next_page = reverse_lazy('inventory:view-login')


class ViewInventory(LoginRequiredMixin, ListView):
    """ Inventory index"""
    login_url = reverse_lazy("inventory:view-login")
    template_name = "index.html"
    context_object_name = "vendors"
    model = Vendors

    def get_queryset(self):
        return self.model.objects.prefetch_related('products').filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ViewInventory, self).get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        context['clients'] = Clients.objects.all()

        return context


class ViewSales(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/sales.html"
    context_object_name = "sales"
    model = Tickets

    def get_queryset(self):
        vendor = Vendors.objects.get(user=self.request.user)
        return self.model.objects.filter(vendor=vendor.id)


class ViewSalesData(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/sales_data.html"
    context_object_name = "clients"
    model = Clients

    def get_queryset(self):
        return self.model.objects.all()


def insert_order_to_db(orders):
    # TODO: Refactor Change unit insertion for Bulk
    order = Orders.objects.create(total=orders['sumTotalAmount'])
    for product_id, value in orders["products"].items():
        product = Products.objects.get(id=product_id)
        order.products.add(product)


def generate_pdf(request, template):
    media_pdf_path = f'{request.user}/pdf/test2.pdf'
    pdf_path = os.path.join(settings.MEDIA_ROOT, media_pdf_path)
    css_path = f'tenants/{request.user}/css/note.css'

    pdf_file = HTML(string=template).write_pdf(
        stylesheets=[CSS(settings.STATIC_ROOT + css_path)],
        presentational_hints=True)

    download_path = f'{request.scheme}://{request.get_host()}/{media_pdf_path}'

    dirname = os.path.dirname(__file__)
    if os.path.exists(dirname):
        f = open(pdf_path, 'wb')
        f.write(pdf_file)

    return download_path


def send_pdf_sms(pdf_path):
    account_sid = 'AC81ecb5361350d7c651828ded7208547e'
    auth_token = '7972d8c260291774f4f491278fc186a9'
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=f'Gracias por tu compra, descarga tu Nota aquí: {pdf_path}',
        from_='+12408984498',
        to='+522382504583'
    )


class ViewNote(LoginRequiredMixin, TemplateView):

    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/note.html"
    orders = {}

    def post(self, request, *args, **kwargs):
        print('Entro al post')
        orders = json.loads(request.body)
        self.orders['orders'] = orders
        insert_order_to_db(orders)
        return reverse_lazy('inventory: view-note')

    def get_context_data(self, **kwargs):
        context = super(ViewNote, self).get_context_data(**kwargs)
        date = datetime.strftime(datetime.now() ,'%b %d, %Y')
        context['products'] = self.orders["orders"]["products"]
        context['total'] = self.orders["orders"]["sumTotalAmount"]
        context["client"] = Clients.objects.get(id=self.orders["orders"]["clientID"])
        context["date"] =  date
        rendered_template = render_to_string(self.template_name, {"products": self.orders["orders"]["products"],
                                                                  "date": date,
                                                                  "total":self.orders["orders"]["sumTotalAmount"] })
        pdf_path = generate_pdf(self.request, rendered_template)

        return context

class ViewInventoryAll(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/inventory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['vendors'] = Vendors.objects.prefetch_related('products').filter(user=self.request.user)

        return context


class ViewCustomers(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/customer/customers.html"
    model = Clients
    context_object_name = "customers"

    def get_queryset(self):
        return self.model.objects.all()


class ViewCreateCustomers(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/customer/new.html"
    success_url = reverse_lazy('inventory:view-customers')
    model = Clients
    form_class = ClientForm


class ViewUpdateCustomers(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/customer/update_client.html"
    success_url = reverse_lazy('inventory:view-customers')
    model = Clients
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']

        return context


class ViewShowOrders(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/orders.html"
    success_url = reverse_lazy('inventory:view-sales')
    model = Orders
    form_class = OrdersForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['data'] = Orders.objects.get(id=self.kwargs['pk'])
        context['orders'] = Orders.objects.prefetch_related('products').filter(id=self.kwargs['pk'])

        return context


class SearchView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "index.html"
    model = Products
    context_object_name = 'productos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        # TODO: Modify query to search only seller's products
        Vendors.objects.prefetch_related('products').filter(user=self.request.user)
        return self.model.objects.filter(name__icontains=query)


class ViewShowProduct(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/products/product_detail.html"
    success_url = reverse_lazy('inventory:view-inventory-all')
    model = Products
    form_class = ProductsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']

        return context


class ViewShowTickets(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/products/ticket_detail.html"
    success_url = reverse_lazy('inventory:view-sales')
    model = Tickets
    form_class = TicketsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']

        return context

