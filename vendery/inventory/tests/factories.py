import factory.fuzzy
from django.core.files.base import ContentFile

from ..models import *


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


class UserFactory(factory.django.DjangoModelFactory):
    address = factory.fuzzy.FuzzyText()
    phone = factory.fuzzy.FuzzyText()
    username = factory.fuzzy.FuzzyText()
    email = factory.LazyAttribute(lambda a: 'test@test.com')

    class Meta:
        model = User


class VendorsFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    phone = factory.fuzzy.FuzzyText()
    status = factory.fuzzy.FuzzyChoice(
        x[0] for x in Vendors.Status.choices
    )
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.products.add(group)

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

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.products.add(group)

    class Meta:
        model = Orders


class TicketsFactory(factory.django.DjangoModelFactory):
    location = factory.fuzzy.FuzzyText()
    comments = factory.fuzzy.FuzzyText()
    debt = factory.fuzzy.FuzzyFloat(0.5, 42.7)
    vendor = factory.SubFactory(VendorsFactory)
    client = factory.SubFactory(ClientsFactory)
    order = factory.SubFactory(OrdersFactory)

    firm = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'nota-remision.png'
        )
    )

    class Meta:
        model = Tickets
