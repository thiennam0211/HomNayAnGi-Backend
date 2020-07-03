# Generated by Django 3.0.5 on 2020-06-24 17:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecipesManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='possible_unit',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='inductions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]