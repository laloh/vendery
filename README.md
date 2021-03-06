Vendery
==============================

Web Application for Inventory Management

### Template Django Project

https://django-tenants.readthedocs.io/en/latest/files.html

### Quick setup

> The next steps assume that poetry is already installed

1 - <a name="step-1">Create a poetry environment:</a>

```bash
poetry lock
poetry install
```

2 - <a name="step-2">Activate the poetry environment</a>

```bash
poetry shell
```

3 - <a name="step-4">Configure the database connection string on the .env</a>

On Linux and Mac

```bash
cp env.sample.mac_or_linux .env

Note: When you're in prod, use the next env variable:
DATABASE_URL=postgres://titan:test1234@localhost:5432/vendery
```

On Windows

```bash
copy env.sample.windows .env
```

Change the value of the variable `DATABASE_URL` inside the file` .env` with the information of the database we want to connect.

Note: Several project settings have been configured so that they can be easily manipulated using environment variables or a plain text configuration file, such as the `.env` file.
This is done with the help of a library called django-environ. We can see the formats expected by `DATABASE_URL` at https://github.com/jacobian/dj-database-url#url-schema. 


4 - <a name="step-4">Install Postgres Locally</a>

```
./dev-tools/install-postgres.sh
sudo service postgresql start
```

5 - <a name="step-5">Use the django-extension's `sqlcreate` management command to help to create the database</a>

On Linux:

```bash
python manage.py sqlcreate | sudo -u postgres psql -U postgres
```

On Mac:

```bash
python manage.py sqlcreate | psql
```

On Windows:

Since [there is no official support for PostgreSQL 12 on Windows 10](https://www.postgresql.org/download/windows/) (officially PostgreSQL 12 is only supported on Windows Server), we choose to use SQLite3 on Windows

6 - <a name="step-6">Run the `migrations` to finish configuring the database to able to run the project</a>


```bash
python manage.py migrate
```


# Create Super User

```
python manage.py createsuperuser

user: admin
password: admin
```

### <a name="running-tests">Running the tests and coverage test</a>


```bash
coverage run -m pytest
```


## <a name="troubleshooting">Troubleshooting</a>

If for some reason you get an error similar to bellow, is because the DATABASE_URL is configured to `postgres:///sina` and because of it the generated `DATABASES` settings are configured to connect on PostgreSQL using the socket mode.
In that case, you must create the database manually because the `sqlcreate` is not capable to correctly generate the SQL query in this case.

```sql
ERROR:  syntax error at or near "WITH"
LINE 1: CREATE USER  WITH ENCRYPTED PASSWORD '' CREATEDB;
                     ^
ERROR:  zero-length delimited identifier at or near """"
LINE 1: CREATE DATABASE sina WITH ENCODING 'UTF-8' OWNER "";
                                                             ^
ERROR:  syntax error at or near ";"
LINE 1: GRANT ALL PRIVILEGES ON DATABASE sina TO ;
```



```sql
ERROR:  role "myuser" already exists
ERROR:  database "sina" already exists
GRANT
```

<a name="troubleshooting-delete-database">You can delete the database and the user with the commands below and then [perform step 5 again](#step-5).</a>

> :warning: **Be very careful here!**: The commands below erase data, and should only be executed on your local development machine and **NEVER** on a production server.


On Linux:

```bash
sudo -u postgres dropdb -U postgres --if-exists sina
sudo -u postgres dropuser -U postgres --if-exists myuser
```

On Mac:

```bash
dropdb --if-exists sina
dropuser --if-exists myuser
```

# Create User
`create user vendery with encrypted password 'test1234';`

# Run Migrations
`python manage.py migrate_schemas --shared`

## Deploy to PROD
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

# Create A Tenant

## LOCAL

```python
from vendery.customers import Client, Domain

# create your public tenant
tenant = Client(schema_name='vendery',
                name='Schemas Inc.',
                paid_until='2016-12-05',
                on_trial=False)
tenant.save()

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'localhost'  # don't add your port or www here! on a local server you'll want to use localhost here
domain.tenant = tenant
domain.is_primary = True
domain.save()

from vendery.customers import Client, Domain

# create your first real tenant
tenant = Client(schema_name='pao',
                name='Fonzy Tenant',
                paid_until='2014-12-05',
                on_trial=True)
tenant.save()  # migrate_schemas automatically called, your tenant is ready to be used!

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'pao.localhost'  # don't add your port or www here!
domain.tenant = tenant
domain.is_primary = True
domain.save()
```

## PROD

```python
from vendery.customers.models import Client, Domain

# create your public tenant
tenant = Client(schema_name='vendery',
                name='Schemas Inc.',
                paid_until='2016-12-05',
                on_trial=False)
tenant.save()

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'vendery.app'  # don't add your port or www here! on a local server you'll want to use localhost here
domain.tenant = tenant
domain.is_primary = True
domain.save()

from vendery.customers.models import Client, Domain

# create your first real tenant
tenant = Client(schema_name='pao',
                name='Fonzy Tenant',
                paid_until='2014-12-05',
                on_trial=True)
tenant.save()  # migrate_schemas automatically called, your tenant is ready to be used!

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'pao.vendery.app'  # don't add your port or www here!
domain.tenant = tenant
domain.is_primary = True
domain.save()
```

# CREATE SUPERUSER FOR A TENANT

`./manage.py create_tenant_superuser`

# Django Jet
config: https://jet.readthedocs.io/en/latest/config_file.html#jet-default-theme

# Factory Boy with Django Tenant
Execute:
`python manage.py tenant_command shell_plus`

then import factory boy. 

i.e.

```python
In [1]: from vendery.inventory.tests.factories import *

In [2]: product = ProductsFactory()

In [3]: product
Out[3]: <Products: joIYNzQPdVQI>

```

# Install Fonts for WeasyToPrint on Linux
````shell
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
````

# Install Fonts for WeasyToPrint on MAC
```
brew install cairo
brew install pango
```

# Run migrations

**Set up models**
- `git checkout util/reset_migration`
- `git checkout HEAD-1`
- `python manage.py makemigrations customers`
- `python manage.py makemigrations inventory`
- `python manage.py migrate_schemas --shared`
- `git checkout HEAD`
- `python manage.py makemigrations customers`
- `python manage.py makemigrations inventory`
- `python manage.py migrate_schemas --shared`
- `python manage.py shell_plus`
- `Create tenant with code above`
