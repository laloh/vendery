from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from vendery.inventory.models import *

from django.shortcuts import render, redirect


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


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


class ViewAdminPanel(SuperUserRequiredMixin, TemplateView):
    """ Admin panel index"""
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/index.html"


class ViewCreateCategory(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/new_category.html"
    success_url = reverse_lazy('panel:view-list-category')
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            ["Categorias", reverse("panel:view-list-category")],
            [
                "Nuevo",
                reverse(
                    "panel:view-create-category"),
            ]
        ]
        return context


class ViewListCategory(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/list_category.html"
    success_url = reverse_lazy('panel:view-create-category')
    context_object_name = "categorys"
    model = Category


class ViewUpdateCategory(SuperUserRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/update_category.html"
    success_url = reverse_lazy('panel:view-list-category')
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]

        context["breadcrumb"] = [
            ["Categorias", reverse("panel:view-list-category")],
            [
                "Configuración",
                reverse(
                    "panel:view-update-category",
                    kwargs={"pk": self.kwargs["pk"]},
                ),
            ]
        ]
        return context


class ViewDeleteCategory(SuperUserRequiredMixin, DeleteView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/delete_category.html"
    success_url = reverse_lazy('panel:view-list-category')
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        context["category"] = Category.objects.get(id=self.kwargs["pk"])

        return context


class ViewListClient(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/client/list_client.html"
    success_url = reverse_lazy('panel:view-create-category')
    context_object_name = "customers"
    model = Clients


class ViewCreateClient(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/client/new_client.html"
    success_url = reverse_lazy('panel:view-list-client')
    model = Clients
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            ["Clientes", reverse("panel:view-list-client")],
            [
                "Nuevo",
                reverse(
                    "panel:view-create-client"),
            ]
        ]
        return context


class ViewUpdateClient(SuperUserRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/client/update_client.html"
    success_url = reverse_lazy('panel:view-list-client')
    model = Clients
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]

        context["breadcrumb"] = [
            ["Clientes", reverse("panel:view-list-client")],
            [
                "Configuración",
                reverse(
                    "panel:view-update-client",
                    kwargs={"pk": self.kwargs["pk"]},
                ),
            ]
        ]
        return context


class ViewDeleteClient(SuperUserRequiredMixin, DeleteView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/client/delete_client.html"
    success_url = reverse_lazy('panel:view-list-client')
    model = Clients

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        context["client"] = Clients.objects.get(id=self.kwargs["pk"])
        return context


class ViewListProducts(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/products/list_product.html"
    success_url = reverse_lazy('panel:view-create-category')
    context_object_name = "products"
    model = Products


class ViewCreateProducts(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/products/new_product.html"
    success_url = reverse_lazy('panel:view-list-product')
    model = Products
    form_class = ProductsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            ["Productos", reverse("panel:view-list-product")],
            [
                "Nuevo",
                reverse(
                    "panel:view-create-product"),
            ]
        ]
        return context


class ViewUpdateProducts(SuperUserRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/products/update_product.html"
    success_url = reverse_lazy('panel:view-list-product')
    model = Products
    form_class = ProductsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]

        context["breadcrumb"] = [
            ["Productos", reverse("panel:view-list-product")],
            [
                "Configuración",
                reverse(
                    "panel:view-update-product",
                    kwargs={"pk": self.kwargs["pk"]},
                ),
            ]
        ]
        return context


class ViewDeleteProducts(SuperUserRequiredMixin, DeleteView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/products/delete_products.html"
    success_url = reverse_lazy('panel:view-list-product')
    model = Products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        context["product"] = Products.objects.get(id=self.kwargs["pk"])

        return context


class ViewListProvider(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/provider/list_provider.html"
    model = Provider
    context_object_name = "providers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            ["Proveedores", reverse("panel:view-list-provider")]
        ]
        return context


class ViewCreateProvider(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/provider/new_provider.html"
    success_url = reverse_lazy('panel:view-list-provider')
    model = Provider
    form_class = ProviderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            ["Proveedores", reverse("panel:view-list-provider")],
            [
                "Nuevo",
                reverse(
                    "panel:view-create-provider"),
            ]
        ]
        return context


class ViewUpdateProvider(SuperUserRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/provider/update_provider.html"
    success_url = reverse_lazy('panel:view-list-provider')
    model = Provider
    form_class = ProviderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]

        context["breadcrumb"] = [
            ["Proveedores", reverse("panel:view-list-provider")],
            [
                "Configuración",
                reverse(
                    "panel:view-update-provider",
                    kwargs={"pk": self.kwargs["pk"]},
                ),
            ]
        ]
        return context


class ViewDeleteProvider(SuperUserRequiredMixin, DeleteView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/provider/delete_provider.html"
    success_url = reverse_lazy('panel:view-list-provider')
    model = Provider

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        context["provider"] = Provider.objects.get(id=self.kwargs["pk"])
        return context


class ViewListVendors(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/vendors/list_vendors.html"
    model = Vendors
    context_object_name = "vendors"


class ViewCreateVendors(SuperUserRequiredMixin, CreateView):
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
                                            email=email, password=password)
            for product_id in products:
                product = Products.objects.get(id=product_id)
                print(product)
                vendor.products.add(product)

        return redirect('panel:view-list-vendors')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            ["Vendedores", reverse("panel:view-list-vendors")],
            [
                "Nuevo",
                reverse(
                    "panel:view-create-vendor"),
            ]
        ]
        return context


class ViewUpdateVendors(SuperUserRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/vendors/update_vendors.html"
    success_url = reverse_lazy('panel:view-list-vendors')
    model = Vendors
    form_class = VendorsForm

    def post(self, request, *args, **kwargs):
        # TODO: improve the way you update sellers
        if request.method == 'POST':
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            status = request.POST.get("status")
            email = request.POST.get("email")
            password = request.POST.get("password")
            products = request.POST.getlist("products")
            vendor = Vendors.objects.get(id=kwargs['pk'])
            user = User.objects.get(id=vendor.user.id)
            user.set_password(password)
            Vendors.objects.filter(id=kwargs['pk']).update(name=name, phone=phone, status=status,
                                            email=email, password=password)
            vendor.products.clear()
            for product_id in products:
                product = Products.objects.get(id=product_id)
                print(product)
                vendor.products.add(product)
            user.save()

        return redirect('panel:view-list-vendors')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]

        context["breadcrumb"] = [
            ["Vendedores", reverse("panel:view-list-vendors")],
            [
                "Configuración",
                reverse(
                    "panel:view-update-vendors",
                    kwargs={"pk": self.kwargs["pk"]},
                ),
            ]
        ]
        return context


class ViewCreateProductSize(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/sizes/new_product_size.html"
    success_url = reverse_lazy('panel:view-list-product-size')
    model = ProductSize
    form_class = ProductSizeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            ["Tallas", reverse("panel:view-list-product-size")],
            [
                "Nuevo",
                reverse(
                    "panel:view-create-product-size"),
            ]
        ]
        return context


class ViewListProductSize(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/sizes/list_product_size.html"
    context_object_name = "sizes"
    model = ProductSize


class ViewDeleteVendor(SuperUserRequiredMixin, DeleteView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/vendors/delete_vendors.html"
    success_url = reverse_lazy('panel:view-list-vendors')
    model = Vendors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        context["vendor"] = Vendors.objects.get(id=self.kwargs["pk"])
        return context


class ViewListExpenses(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/expenses/list_expenses.html"
    model = Expenses
    context_object_name = "expenses"


class ViewUpdateExpenses(SuperUserRequiredMixin, UpdateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/expenses/update_expense.html"
    success_url = reverse_lazy('panel:view-list-expenses')
    model = Expenses
    form_class = ExpensesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]

        context["breadcrumb"] = [
            ["Gastos", reverse("panel:view-list-expenses")],
            [
                "Configuración",
                reverse(
                    "panel:view-update-expenses",
                    kwargs={"pk": self.kwargs["pk"]},
                ),
            ]
        ]
        return context


class ViewCreateExpenses(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/expenses/new_expense.html"
    success_url = reverse_lazy('panel:view-list-expenses')
    model = Expenses
    form_class = ExpensesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            ["Gastos", reverse("panel:view-list-expenses")],
            [
                "Nuevo",
                reverse(
                    "panel:view-create-expenses"),
            ]
        ]
        return context


class ViewDeleteExpense(SuperUserRequiredMixin, DeleteView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/expenses/delete_expense.html"
    success_url = reverse_lazy('panel:view-list-expenses')
    model = Expenses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        context["expense"] = Expenses.objects.get(id=self.kwargs["pk"])
        return context


class ViewListSells(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy("panel:view-login-panel")
    template_name = "admin_panel/views/sells/list_sells.html"
    context_object_name = "sells"
    model = Sales
