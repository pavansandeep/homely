# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=32, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OwnerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
                ('primary_contact_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{10}$', message=b'Phone number must be a 10 digit number.')])),
                ('primary_contact_type', models.CharField(default='Home', max_length=10, choices=[('Home', 'Home'), ('Mobile', 'Mobile'), ('Office', 'Office')])),
                ('secondary_contact_number', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{10}$', message=b'Phone number must be a 10 digit number.')])),
                ('secondary_contact_type', models.CharField(default='Mobile', max_length=10, null=True, blank=True, choices=[('Home', 'Home'), ('Mobile', 'Mobile'), ('Office', 'Office')])),
                ('primary_address', models.ForeignKey(related_name='owner_profiles_primary', to='rental.Address')),
                ('secondary_address', models.ForeignKey(related_name='owner_profiles_secondary', blank=True, to='rental.Address', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('rental_price', models.DecimalField(max_digits=18, decimal_places=3)),
                ('bedroom_count', models.PositiveIntegerField(default=0)),
                ('location', models.OneToOneField(to='rental.Address')),
                ('owner', models.ForeignKey(related_name='properties', to='rental.OwnerProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RenterProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
                ('primary_contact_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{10}$', message=b'Phone number must be a 10 digit number.')])),
                ('primary_contact_type', models.CharField(default='Home', max_length=10, choices=[('Home', 'Home'), ('Mobile', 'Mobile'), ('Office', 'Office')])),
                ('secondary_contact_number', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{10}$', message=b'Phone number must be a 10 digit number.')])),
                ('secondary_contact_type', models.CharField(default='Mobile', max_length=10, null=True, blank=True, choices=[('Home', 'Home'), ('Mobile', 'Mobile'), ('Office', 'Office')])),
                ('primary_address', models.ForeignKey(related_name='renter_profiles_primary', to='rental.Address')),
                ('secondary_address', models.ForeignKey(related_name='renter_profiles_secondary', blank=True, to='rental.Address', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('rental_price', models.DecimalField(max_digits=18, decimal_places=3)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('notes', models.TextField(null=True, blank=True)),
                ('property', models.ForeignKey(related_name='reservations', to='rental.Property')),
                ('renter', models.ForeignKey(related_name='reservations', to='rental.RenterProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
