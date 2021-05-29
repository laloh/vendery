# Generated by Django 3.1.11 on 2021-05-29 03:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(default=None, max_length=255)),
                ('status', models.CharField(choices=[('available', 'Available'), ('deleted', 'Deleted'), ('paused', 'Paused'), ('out_of_stock', 'Out of stock')], default='available', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(default=None, max_length=255)),
                ('phone', models.CharField(default=None, max_length=20)),
                ('email', models.CharField(default=None, max_length=255)),
                ('password', models.CharField(default=None, max_length=255)),
                ('location', models.CharField(default=None, max_length=255)),
                ('store_name', models.CharField(default=None, max_length=255)),
                ('debt', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('available', 'Available'), ('deleted', 'Deleted'), ('paused', 'Paused')], default='available', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('total', models.FloatField(default=0)),
                ('store', models.CharField(default=None, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(default=None, max_length=255)),
                ('price', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('available', 'Available'), ('deleted', 'Deleted'), ('paused', 'Paused'), ('out_of_stock', 'Out of stock')], default='available', max_length=50)),
                ('description', models.TextField(default=None)),
                ('stock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(default=None, max_length=255)),
                ('phone', models.CharField(default=None, max_length=20)),
                ('email', models.CharField(default=None, max_length=255)),
                ('password', models.CharField(default=None, max_length=255)),
                ('status', models.CharField(choices=[('available', 'Available'), ('deleted', 'Deleted'), ('paused', 'Paused')], default='available', max_length=50)),
                ('products', models.ManyToManyField(to='inventory.Products')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('firm', models.ImageField(default=None, upload_to='')),
                ('location', models.CharField(default=None, max_length=255)),
                ('comments', models.TextField(default=None)),
                ('debt', models.FloatField(default=0)),
                ('client', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='inventory.clients')),
                ('order', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='inventory.orders')),
                ('vendor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='inventory.vendors')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='products',
            field=models.ManyToManyField(to='inventory.Products'),
        ),
    ]