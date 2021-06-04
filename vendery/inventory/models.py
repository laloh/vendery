from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser


class Category (TimeStampedModel):

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        DELETED = "deleted", "Deleted"
        PAUSED = "paused", "Paused"
        OUT_OF_STOCK = "out_of_stock", "Out of stock"

    name = models.CharField(max_length=255, default=None)
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE, max_length=50)

    class Meta:
        verbose_name = ('Categoria')
        verbose_name_plural = ('Categorias')

    def __str__(self):
        return self.name


class Products(TimeStampedModel):

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        DELETED = "deleted", "Deleted"
        PAUSED = "paused", "Paused"
        OUT_OF_STOCK = "out_of_stock", "Out of stock"

    name = models.CharField(max_length=255, default=None)
    price = models.FloatField(default=0)
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE, max_length=50)
    description = models.TextField(default=None)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = ('Producto')
        verbose_name_plural = ('Productos')

    def __str__(self):
        return self.name


class User(AbstractUser, TimeStampedModel):
    # TODO:
    direccion = models.TextField(blank=True, max_length=50)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return '{}'.format(self.direccion)


class Vendors(TimeStampedModel):
    # TODO: Add Gastos Field
    # TODO: See if we can delete password field
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        DELETED = "deleted", "Deleted"
        PAUSED = "paused", "Paused"

    name = models.CharField(max_length=255, default=None)
    phone = models.CharField(max_length=20, default=None)
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE, max_length=50)
    products = models.ManyToManyField(Products)

    class Meta:
        verbose_name = ('Vendedor')
        verbose_name_plural = ('Vendedores')

    def __str__(self):
        return self.name


class Clients(TimeStampedModel):
    # TODO: See if we can delete password field
    # TODO: Maximize location by form

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        DELETED = "deleted", "Deleted"
        PAUSED = "paused", "Paused"

    name = models.CharField(max_length=255, default=None)
    phone = models.CharField(max_length=20, default=None)
    email = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=255, default=None)
    location = models.CharField(max_length=255, default=None)
    store_name = models.CharField(max_length=255, default=None)
    debt = models.FloatField(default=0)
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE, max_length=50)

    class Meta:
        verbose_name = ('Cliente')
        verbose_name_plural = ('Clientes')

    def __str__(self):
        return self.name


class Orders(TimeStampedModel):

    total = models.FloatField(default=0)
    store = models.CharField(default=None, max_length=255)
    products = models.ManyToManyField(Products)

    class Meta:
        verbose_name = ('Venta')
        verbose_name_plural = ('Ventas')

    def __str__(self):
        return "Orders"


class Tickets(TimeStampedModel):

    firm = models.ImageField(default=None)
    location = models.CharField(max_length=255, default=None)
    comments = models.TextField(default=None)
    debt = models.FloatField(default=0)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, default=None)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, default=None)
    order = models.OneToOneField(Orders, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = ('Ticket')
        verbose_name_plural = ('Tickets')

    def __str__(self):
        return "Firm from Admin"
