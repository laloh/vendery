from django.db import models
from model_utils.models import TimeStampedModel


class Category (TimeStampedModel):

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        DELETED = "deleted", "Deleted"
        PAUSED = "paused", "Paused"
        OUT_OF_STOCK = "out_of_stock", "Out of stock"

    name = models.CharField(max_length=255, default=None)
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE, max_length=50)

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
    email = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=255, default=None)
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE, max_length=50)
    products = models.ManyToManyField(Products)

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

    def __str__(self):
        return self.name


class Orders(TimeStampedModel):

    total = models.FloatField(default=0)
    store = models.CharField(default=None, max_length=255)
    products = models.ManyToManyField(Products)

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

    def __str__(self):
        return "Firm from Admin"
