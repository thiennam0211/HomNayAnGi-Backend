# Generated by Django 3.0.5 on 2020-07-17 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usermanager', '0001_initial'),
        ('RecipesManager', '0008_auto_20200717_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('unit', models.CharField(max_length=1024)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('update_at', models.DateTimeField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='RecipesManager.Ingredients')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='usermanager.Users')),
            ],
            options={
                'unique_together': {('user', 'food')},
            },
        ),
    ]
