from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from vendery.inventory.models import *

class AuthenticationFormUserPanel(AuthenticationForm):
    def clean(self):
        if self.cleaned_data is None:
            self.add_error('username', "Ingrese un email")
            self.add_error('password', "Ingrese un password")
            return False

        if not self.cleaned_data:
            self.add_error('username', "Ingrese un email")
            self.add_error('password', "Ingrese un password")
            return False

        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not email:
            self.add_error('username', "Ingrese un email")
            return False

        if not password:
            self.add_error('password', "Ingrese una contraseña")
            return False

        _user_est = User.objects.filter(email=email)

        if not _user_est.exists():
            self.add_error('username', "El email no esta registrado")
            return False

        _user = _user_est[0]


        if _user:
            self.user_cache = authenticate(self.request, username=_user.username, password=password)

        else:
            raise forms.ValidationError(
                'No tiene permisos para entrar al sistema',
                code='invalid_login',
                params={'email': email},
            )

        if self.user_cache is None:
            raise forms.ValidationError(
                'Los datos proporcionados no son correctos',
                code='invalid_login',
                params={'username': email},
            )
        self.cleaned_data['username'] = _user.username
        return self.cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = "__all__"


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = "__all__"


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = "__all__"


class TicketsForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = "__all__"


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = "__all__"


class VendorsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Vendors
        fields = "__all__"
