# TODO: Add validation when is on PROD.
# IDK Why but you need to add two lines at the end to run correctly
# Run: python manage.py tenant_command shell_plus -s pao < dev-utils/delete-fake-data.py
print("Eliminando Category....")
Category.objects.all().delete()

print("Eliminando Products....")
print(Products.objects.all().delete())

print("Eliminando User....")
print(User.objects.all().delete())

print("Eliminando Vendors....")
print(Vendors.objects.all().delete())

print("Eliminando Clients....")
print(Clients.objects.all().delete())

print("Eliminando Orders....")
print(Orders.objects.all().delete())

print("Eliminando Tickets....")
print(Tickets.objects.all().delete())

