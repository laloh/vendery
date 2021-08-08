echo "Deleting Migrations files"
eval `find . -path "*/migrations/*.pyc"  -delete`
eval `find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`

echo "Deleting Vendery Database"
eval `sudo -u postgres dropdb -U postgres --if-exists vendery`

echo "Create Vendery Database"
eval `python manage.py sqlcreate | sudo -u postgres psql -U postgres`
