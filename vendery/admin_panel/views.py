from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from vendery.inventory.models import *

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
    model = Tickets


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


class ViewListProvider(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/provider/list_provider.html"
    model = Provider
    context_object_name = "providers"


class ViewCreateProvider(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/provider/new_provider.html"
    success_url = reverse_lazy('panel:view-list-provider')
    model = Provider
    form_class = ProviderForm


class ViewUpdateProvider(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/provider/update_provider.html"
    success_url = reverse_lazy('panel:view-list-provider')
    model = Provider
    form_class = ProviderForm


class ViewListVendors(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/vendors/list_vendors.html"
    model = Vendors
    context_object_name = "vendors"


class ViewCreateVendors(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/vendors/new_vendors.html"
    success_url = reverse_lazy('panel:view-list-vendors')
    model = Vendors
    form_class = VendorsForm

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            status = request.POST.get("status")
            email = request.POST.get("email")
            password = request.POST.get("password")
            products = request.POST.getlist("products")
            print(products)
            user = User.objects.create_user(username=name,
                                            email=email,
                                            password=password)
            vendor = Vendors.objects.create(user=user, name=name, phone=phone, status=status,
                                            email=email, password='testing321')
            for product_id in products:
                product = Products.objects.get(id=product_id)
                print(product)
                vendor.products.add(product)

        return redirect('panel:view-list-vendors')


class ViewUpdateVendors(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/vendors/update_vendors.html"
    success_url = reverse_lazy('panel:view-list-vendors')
    model = Vendors
    form_class = VendorsForm