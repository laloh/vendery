from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import AuthenticationFormUser
from .models import Vendors, Tickets, Clients, Products


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


class ViewNote(LoginRequiredMixin, TemplateView):
    template_name = "views/note.html"


class ViewInventoryAll(LoginRequiredMixin, TemplateView):
    template_name = "views/inventory.html"


class ViewCustomers(LoginRequiredMixin, ListView):
    template_name = "views/customers.html"
    model = Clients
    context_object_name = "customers"

    def get_queryset(self):
        return self.model.objects.all()


