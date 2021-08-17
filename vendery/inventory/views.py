import os
import json
import re
import uuid

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
from twilio.rest import Client
from datetime import date
from datetime import datetime

from .forms import *
from .models import (
    Vendors,
    Tickets,
    Clients,
    Products,
    Orders,
    TemporaryOrders,
    Expenses,
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
    context_object_name = "sales"
    model = Tickets

    def get_queryset(self):
        vendor = Vendors.objects.get(user=self.request.user)
        return self.model.objects.filter(vendor=vendor.id)

    def get_context_data(self, *args, **kwargs):
        context = super(ViewSales, self).get_context_data(**kwargs)
        context[
            "pdf"
        ] = f"{self.request.scheme}://{self.request.get_host()}/{self.request.tenant.schema_name}/pdf/order_"
        return context


class ViewSalesData(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/sales_data.html"
    context_object_name = "clients"
    model = Clients

    def get_queryset(self):
        return self.model.objects.all()


def insert_order_to_db(orders):
    # TODO: Refactor Change unit insertion for Bulk
    order = Orders.objects.create(total=orders["sumTotalAmount"])
    for product_id, value in orders["products"].items():
        product = Products.objects.get(id=product_id)
        order.products.add(product)


def generate_pdf(request, template, token):
    unique_id = uuid.uuid4().hex[:8]
    media_pdf_path = f"{request.tenant.schema_name}/pdf/order_{token}.pdf"
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


class ViewNote(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/product_orders.html"

    def post(self, request, *args, **kwargs):
        orders = json.loads(request.body)
        user_id = self.request.user
        token = kwargs["token"]
        TemporaryOrders.objects.create(unique_id=token, data_orders=orders)
        total = orders["sumTotalAmount"]
        productos = orders["products"]
        object_order = Orders.objects.create(total=total)
        for key, value in productos.items():
            product = Products.objects.get(id=key)
            object_order.products.add(product)
        user = Vendors.objects.get(user=user_id)
        client = Clients.objects.get(id=orders["clientID"])
        Tickets.objects.create(
            vendor=user, client=client, order=object_order, token=token
        )
        return redirect("inventory:view-sales")

    def get_context_data(self, *args, **kwargs):
        context = super(ViewNote, self).get_context_data(**kwargs)
        context["token"] = self.kwargs["token"]
        print("tok", self.kwargs["token"])
        return context


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


class ViewShowOrders(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/orders.html"
    success_url = reverse_lazy("inventory:view-sales")
    model = Orders
    form_class = OrdersForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["data"] = Orders.objects.get(id=self.kwargs["pk"])
        context["orders"] = Orders.objects.prefetch_related("products").filter(
            id=self.kwargs["pk"]
        )

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


class ViewShowTickets(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/products/ticket_detail.html"
    success_url = reverse_lazy("inventory:view-sales")
    model = Tickets
    form_class = TicketsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["pk"] = self.kwargs["pk"]

        return context


class ViewTemporaryOrders(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("inventory:view-login")
    template_name = "views/note.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ViewTemporaryOrders, self).get_context_data(**kwargs)
        date = datetime.strftime(datetime.now(), '%d/%m/%Y')
        datos = TemporaryOrders.objects.get(unique_id=self.kwargs['token'])
        id_client = datos.data_orders["clientID"]
        client = Clients.objects.get(id=id_client)
        print("dude what the fuck is going on")
        user = self.request.user
        context["products"] = datos.data_orders["products"]
        context["total"] = datos.data_orders["sumTotalAmount"]
        context["client"] = client
        context["date"] = date
        context['vendor'] = user
        token = kwargs['token']
        rendered_template = render_to_string(self.template_name, {"products": datos.data_orders['products'],
                                                                  "date": date,
                                                                  "total": datos.data_orders["sumTotalAmount"],
                                                                  "vendor": user,
                                                                  "client": client,
                                                                  "token": token,
                                                                  "vendor": user})
        pdf_path = generate_pdf(self.request, rendered_template, token)
        send_pdf_sms(pdf_path, client.phone)
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
