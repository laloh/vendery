# IDK Why but you need to add two lines at the end to run correctly
# Run: python manage.py tenant_command shell_plus -s pao < dev-utils/generate-fake-data.py
from vendery.inventory.tests.factories import *

for i in range(0, 10):
    print(f"Generando Categoria {i}:", CategoryFactory())

products = []
for i in range(0, 10):
    print(f"Generando Producto {i}:", products.append(ProductsFactory()))

for i in range(0, 10):
    print(f"Generando Usuario {i}:", UserFactory())

for i in range(0, 10):
    print(f"Generando Vendedor {i}:", VendorsFactory.create(products=products))

for i in range(0, 10):
    print(f"Generando Cliente {i}:", ClientsFactory())

for i in range(0, 10):
    print(f"Generando Ordenes (ventas) {i}:", OrdersFactory.create(products=products[:5]))

for i in range(0, 10):
    print(f"Generando Ticket (Nota de remision) {i}:", TicketsFactory())

