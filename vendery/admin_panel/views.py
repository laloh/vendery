from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthenticationFormUserPanel


class LoginPanel(LoginView):
    template_name = 'admin_panel/login_admin.html'
    authentication_form = AuthenticationFormUserPanel
    success_url = reverse_lazy('panel:view-admin-panel')

    # redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('panel:view-admin-panel'))
        else:
            return super(LoginPanel, self).get(request, *args, **kwargs)


class LogoutPanel(LogoutView):
    next_page = reverse_lazy('panel:view-login-panel')


class ViewAdminPanel(LoginRequiredMixin, TemplateView):
    """ Admin panel index"""
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/index.html"
