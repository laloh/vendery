from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Category(TimeStampedModel):

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
    # TODO: Add Labels to spanish
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        DELETED = "deleted", "Deleted"
        PAUSED = "paused", "Paused"
        OUT_OF_STOCK = "out_of_stock", "Out of stock"

    name = models.CharField(max_length=255, default=None)
    price = models.FloatField(default=0)
    # TODO Make it optional
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE, max_length=50)
    description = models.TextField(default=None)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    image = ResizedImageField(default=None)

    class Meta:
        verbose_name = ('Producto')
        verbose_name_plural = ('Productos')

    def __str__(self):
        return self.name


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
    products = models.ManyToManyField(Products, related_name='vendors_products')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    email = models.EmailField()
    password = models.CharField(max_length=30, null=True, blank=True)

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
    location = models.CharField(max_length=255, default=None)
    # TODO: Add store_name as Table
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
    products = models.ManyToManyField(Products)

    class Meta:
        verbose_name = ('Venta')
        verbose_name_plural = ('Ventas')

    def __str__(self):
        return str(self.id)


class Tickets(TimeStampedModel):

    firm = ResizedImageField(default=None)
    location = models.CharField(max_length=255, default=None, blank=True,  null=True)
    comments = models.TextField(default=None, blank=True,  null=True)
    debt = models.FloatField(default=0, blank=True,  null=True)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, default=None)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, default=None)
    order = models.OneToOneField(Orders, on_delete=models.CASCADE, default=None)
    token = models.UUIDField(default=None, unique=True, null=True)

    class Meta:
        verbose_name = ('Ticket')
        verbose_name_plural = ('Tickets')

    def __str__(self):
        return f"{self.id}"


class TemporaryOrders(TimeStampedModel):
    unique_id = models.UUIDField(default=None, unique=True, null=True)
    data_orders = models.JSONField(null=True)

    def __str__(self):
        return f'{self.id}/{self.unique_id}'


class Provider(TimeStampedModel):
    name = models.CharField(max_length=255, default=None)
    phone = models.CharField(max_length=20, default=None)
    email = models.CharField(max_length=255, default=None)
    debt = models.FloatField(default=0, blank=True,  null=True)
    saldo = models.FloatField(default=0, blank=True,  null=True)
    # TODO: modify or verify which products are
    # products = models.ManyToManyField(Products, related_name='provider_products')

    def __str__(self):
        return f'{self.id}/{self.name}'


class Expenses(TimeStampedModel):
    amount = models.FloatField(default=0)
    reason = models.CharField(max_length=255, default=None)
    comments = models.TextField(default=None, blank=True, null=True)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.id}/{self.reason}'