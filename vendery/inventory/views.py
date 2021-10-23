import os
import json
import re
import uuid

from django.http import HttpResponse
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

from .forms import *
from .models import (
    Vendors,
    Clients,
    Products,
    Expenses,
    Sales
)


class Login(LoginView):
    template_name = "login.html"
    authentication_form = AuthenticationFormUser
    success_url = reverse_lazy("inventory:view-inventory")
    redirect_authenticated_user = True

    def get_success_url(self):
        url = super().get_redirect_url()
        return url or self.success_url


class Logout(LogoutView):
    next_page = reverse_lazy("inventory:view-login")


class ViewInventory(LoginRequiredMixin, ListView):
    """Inventory index"""

    login_url = reverse_lazy("inventory:view-login")
    template_name = "index.html"
    context_object_name = "vendors"
    model = Vendors

    def get_queryset(self):
        return self.model.objects.prefetch_related("products").filter(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super(ViewInventory, self).get_context_data(**kwargs)
        context["token"] = uuid.uuid4()
        context["products"] = Products.objects.all()
        context["clients"] = Clients.objects.all()

        return context


class ViewSales(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/sales.html"
    model = Sales

    def get_context_data(self, *, object_list=None, **kwargs):
        sales = Sales.objects.filter(vendor_id=self.request.user.id)
        client = Clients.objects.get(id=sales.first().client_id)
        context = {'sales': sales, 'client_name': client.name}
        print(context)
        return context


class ViewSalesData(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/sales_data.html"
    context_object_name = "clients"
    model = Clients

    def get_queryset(self):
        return self.model.objects.all()


def generate_pdf(request, template, unique_id):
    media_pdf_path = f"{request.tenant.schema_name}/pdf/order_{unique_id}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, media_pdf_path)
    # TODO: Generate Ticket Table Row
    css_path = f"tenants/{request.tenant.schema_name}/css/note.css"
    pdf_file = HTML(string=template).write_pdf(
        stylesheets=[CSS(settings.STATIC_ROOT + css_path)], presentational_hints=True
    )

    download_path = f"{request.scheme}://{request.get_host()}/{media_pdf_path}"

    dirname = os.path.dirname(__file__)
    if os.path.exists(dirname):
        f = open(pdf_path, "wb")
        f.write(pdf_file)

    return download_path


def send_pdf_sms(pdf_path, phone):
    account_sid = "AC81ecb5361350d7c651828ded7208547e"
    auth_token = "7972d8c260291774f4f491278fc186a9"
    client = Client(account_sid, auth_token)

    characters_to_remove = "-() "
    pattern = "[" + characters_to_remove + "]"
    phone = re.sub(pattern, "", phone).replace("+52", "")

    client.messages.create(
        body=f"Gracias por tu compra, descarga tu Nota aquí: {pdf_path}",
        from_="+12408984498",
        to=f"+52{phone}",
    )


# TODO: Send pdf button
# TODO: Buy sellphone to send messages to the clients
# TODO: Agregar modal para los clients cuando se le de click
# TODO: Automatizar el crear el admin, con un bash script o algo asi
# TODO: Arreglar productos panel
# TODO: Merge a master y sacar nueva rama
# TODO: Deploy to PROD, try to recreate a github action
# TODO: Check JS Files load first than HTML
class ViewSendNote(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("inventory:view-login")

    def post(self, request, *args, **kwargs):
        response = {'status': 200, 'message': ("Your error")}
        body = json.loads(request.body)

        pdf_path = body['pdf_url']

        client = Clients.objects.get(id=int(body['client_id']))
        client_phone = client.phone

        send_pdf_sms(pdf_path, client_phone)

        return HttpResponse(json.dumps(response), content_type='application/json')


class ViewNote(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/note.html"

    def post(self, request, *args, **kwargs):
        response = {'status': 200, 'message': ("Your error")}
        unique_id = uuid.uuid4().hex[:8]
        orders = json.loads(request.body)
        orders['vendor'] = self.request.user.id

        products = []
        context = {'client': Clients.objects.get(id=orders['clientID']),
                   'date': datetime.strftime(datetime.now(), '%d/%m/%Y'),
                   'vendor': orders['vendor'],
                   'total': orders['sumTotalAmount'],
                   'uuid': unique_id,
                   }

        # Build Context to render PDF
        for product_id, product_id_body in orders['products'].items():
            for product_size, product_size_body in product_id_body.items():
                products.append({
                    'size': product_size,
                    'name': product_size_body['name'],
                    'price': product_size_body['price'],
                    'quantity': product_size_body['quantity'],
                    'subtotal': product_size_body['subtotal']
                })

        context['products'] = products

        rendered_template = render_to_string(self.template_name, context=context)
        pdf_path = generate_pdf(self.request, rendered_template, unique_id)

        Sales(data=orders,
              vendor_id=orders['vendor'],
              client_id=orders['clientID'],
              total=orders['sumTotalAmount'],
              pdf=pdf_path
              ).save()

        # send_pdf_sms(pdf_path, context['client'].phone)

        return HttpResponse(json.dumps(response), content_type='application/json')


class ViewInventoryAll(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/inventory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["vendors"] = Vendors.objects.prefetch_related("products").filter(
            user=self.request.user
        )

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
    success_url = reverse_lazy("inventory:view-customers")
    model = Clients
    form_class = ClientForm


class ViewUpdateCustomers(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/customer/update_client.html"
    success_url = reverse_lazy("inventory:view-customers")
    model = Clients
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["pk"] = self.kwargs["pk"]

        return context


class SearchView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "index.html"
    model = Products
    context_object_name = "productos"

    def get_queryset(self):
        query = self.request.GET.get("q")
        # TODO: Modify query to search only seller's products
        Vendors.objects.prefetch_related("products").filter(user=self.request.user)
        return self.model.objects.filter(name__icontains=query)


class ViewShowProduct(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/products/product_detail.html"
    success_url = reverse_lazy("inventory:view-inventory-all")
    model = Products
    form_class = ProductsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["pk"] = self.kwargs["pk"]

        return context


class ViewListExpenses(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/expenses/list_expenses.html"
    context_object_name = "expenses"
    model = Expenses

    def get_queryset(self):
        today = date.today()
        vendor = Vendors.objects.get(user=self.request.user)
        return self.model.objects.filter(vendor=vendor, creation_date=today)


class ViewCreateExpenses(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/expenses/new_expenses.html"
    model = Expenses
    form_class = ExpensesForm
    success_url = reverse_lazy("inventory:view-list-expenses")

    def get_context_data(self, *args, **kwargs):
        context = super(ViewCreateExpenses, self).get_context_data(**kwargs)

        context["vendor"] = Vendors.objects.get(user=self.request.user)

        return context


class ViewUpdateExpenses(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/expenses/update_expenses.html"
    success_url = reverse_lazy("inventory:view-list-expenses")
    model = Expenses
    form_class = ExpensesForm

    def get_context_data(self, *args, **kwargs):
        context = super(ViewUpdateExpenses, self).get_context_data(**kwargs)
        context["vendor"] = Vendors.objects.get(user=self.request.user)

        return context


class Error404(TemplateView):
    template_name = "404.html"


class Error500(TemplateView):
    template_name = "500.html"
