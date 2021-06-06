from customers.models import Client, Domain

# create your public tenant
tenant = Client(schema_name='vendery',
                name='Schemas Inc.',
                paid_until='2016-12-05',
                on_trial=False)
tenant.save()

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'localhost' # don't add your port or www here! on a local server you'll want to use localhost here
domain.tenant = tenant
domain.is_primary = True
domain.save()

from customers.models import Client, Domain

# create your first real tenant
tenant = Client(schema_name='pao',
                name='Fonzy Tenant',
                paid_until='2014-12-05',
                on_trial=True)
tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'pao.localhost' # don't add your port or www here!
domain.tenant = tenant
domain.is_primary = True
domain.save()