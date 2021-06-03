import factory
import factory.fuzzy
from django.db.utils import ConnectionRouter

from ..models import Products, Category


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    status = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Category.Status.choices]
    )

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory):
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
