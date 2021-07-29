from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthenticationFormUserPanel, CategoryForm, ClientForm, ProductsForm, TicketsForm, OrdersForm
from vendery.inventory.models import Category, Clients, Products, Tickets, Orders
from django.shortcuts import render, redirect


class LoginPanel(LoginView):
    template_name = 'admin_panel/login_admin.html'
    authentication_form = AuthenticationFormUserPanel
    success_url = reverse_lazy('panel:view-admin-panel')
    redirect_authenticated_user = True

    def get_success_url(self):
        url = super().get_redirect_url()
        return url or self.success_url


class LogoutPanel(LogoutView):
    next_page = reverse_lazy('panel:view-login-panel')


class ViewAdminPanel(LoginRequiredMixin, TemplateView):
    """ Admin panel index"""
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/index.html"


class ViewCreateCategory(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/new_category.html"
    success_url = reverse_lazy('panel:view-create-category')
    model = Category
    form_class = CategoryForm


class ViewListCategory(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/list_category.html"
    success_url = reverse_lazy('panel:view-create-category')
    context_object_name = "categorys"
    model = Category


class ViewUpdateCategory(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/update_category.html"
    success_url = reverse_lazy('panel:view-list-category')
    model = Category
    form_class = CategoryForm


class ViewListClient(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/client/list_client.html"
    success_url = reverse_lazy('panel:view-create-category')
    context_object_name = "customers"
    model = Clients


class ViewCreateClient(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/client/new_client.html"
    success_url = reverse_lazy('panel:view-list-client')
    model = Clients
    form_class = ClientForm


class ViewUpdateClient(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/client/update_client.html"
    success_url = reverse_lazy('panel:view-list-client')
    model = Clients
    form_class = ClientForm


class ViewListProducts(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/products/list_product.html"
    success_url = reverse_lazy('panel:view-create-category')
    context_object_name = "products"
    model = Products


class ViewCreateProducts(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/products/new_product.html"
    success_url = reverse_lazy('panel:view-list-product')
    model = Products
    form_class = ProductsForm


class ViewUpdateProducts(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/products/update_product.html"
    success_url = reverse_lazy('panel:view-list-product')
    model = Products
    form_class = ProductsForm


class ViewListTickets(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/tickets/list_tickets.html"
    context_object_name = "tickets"
    model = Products


class ViewCreateTickets(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/tickets/new_tickets.html"
    success_url = reverse_lazy('panel:view-list-tickets')
    model = Tickets
    form_class = TicketsForm


class ViewUpdateTickets(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/tickets/update_tickets.html"
    success_url = reverse_lazy('panel:view-list-tickets')
    model = Tickets
    form_class = TicketsForm


class ViewListSales(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/sales/list_sales.html"
    context_object_name = "sales"
    model = Orders


class ViewCreateSales(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/sales/new_sale.html"
    success_url = reverse_lazy('panel:view-list-sales')
    model = Orders
    form_class = OrdersForm


class ViewUpdateSales(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/sales/update_sale.html"
    success_url = reverse_lazy('panel:view-list-sales')
    model = Orders
    form_class = OrdersForm
