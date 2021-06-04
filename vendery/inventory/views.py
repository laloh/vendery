from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import AuthenticationFormUser


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


class ViewInventory(LoginRequiredMixin, TemplateView):
    """ Inventory index"""
    login_url = reverse_lazy("inventory:view-login")
    template_name = "index.html"

