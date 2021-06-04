import factory
import factory.fuzzy
from django.db.utils import ConnectionRouter

from ..models import Products, Category, Vendors, Clients, Orders, Tickets


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    status = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Category.Status.choices]
    )

    class Meta:
        model = Category


class ProductsFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    price = factory.fuzzy.FuzzyFloat(0.5, 42.7)
    status = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Products.Status.choices]
    )
    description = factory.fuzzy.FuzzyText()
    stock = factory.fuzzy.FuzzyInteger(0, 10)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Products


class VendorsFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    phone = factory.fuzzy.FuzzyText()
    email = factory.fuzzy.FuzzyText()
    password = factory.fuzzy.FuzzyText()
    status = factory.fuzzy.FuzzyChoice(
        x[0] for x in Vendors.Status.choices
    )

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(Products)

    class Meta:
        model = Vendors


class ClientsFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    phone = factory.fuzzy.FuzzyText()
    email = factory.fuzzy.FuzzyText()
    location = factory.fuzzy.FuzzyText()
    store_name = factory.fuzzy.FuzzyText()
    debt = factory.fuzzy.FuzzyFloat(0.5, 42.7)
    status = factory.fuzzy.FuzzyChoice(
        x[0] for x in Clients.Status.choices
    )

    class Meta:
        model = Clients


class OrdersFactory(factory.django.DjangoModelFactory):
    total = factory.fuzzy.FuzzyFloat(0.5, 42.7)
    store = factory.fuzzy.FuzzyText()
    products = factory.SubFactory(ProductsFactory)

    class Meta:
        model = Orders


class TicketsFactory(factory.django.DjangoModelFactory):
    firm = factory.django.ImageField(from_path='nota-remision.png')
    location = factory.fuzzy.FuzzyText()
    comments = factory.fuzzy.FuzzyText()
    debt = factory.fuzzy.FuzzyFloat(0.5, 42.7)
    vendor = factory.SubFactory(VendorsFactory)
    client = factory.SubFactory(ClientsFactory)
    order = factory.SubFactory(OrdersFactory)

    class Meta:
        model = Tickets
