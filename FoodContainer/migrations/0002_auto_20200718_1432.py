# Generated by Django 3.0.5 on 2020-07-18 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodContainer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='update_at',
        ),
        migrations.AddField(
            model_name='food',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
