# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency_code', models.CharField(max_length=8)),
                ('country_code', models.CharField(max_length=3)),
                ('agency_site_key', models.CharField(db_index=True, max_length=12)),
                ('local_id', models.CharField(db_index=True, max_length=3)),
                ('facility_type', models.CharField(max_length=12)),
                ('effective_date', models.DateTimeField(verbose_name='Record Effective Date')),
                ('city', models.CharField(max_length=64)),
                ('facility_name', models.CharField(max_length=64)),
                ('elevation', models.IntegerField()),
                ('elevation_units', models.CharField(max_length=2)),
                ('tpa_agl', models.IntegerField(verbose_name='Traffic Pattern Altitude (TPA), distance above ground (AGL)')),
                ('tpa_agl_units', models.CharField(max_length=2)),
                ('magnetic_variation_degrees', models.IntegerField()),
                ('magnetic_variation_direction', models.CharField(max_length=2)),
                ('magnetic_variation_year', models.IntegerField()),
                ('ctaf_frequency', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Common Traffic Advisory Frequency (CTAF)')),
                ('icao_id', models.CharField(db_index=True, max_length=4)),
                ('is_public_use', models.NullBooleanField()),
            ],
        ),
    ]
