# Generated by Django 5.0.6 on 2024-06-05 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mealcode',
            options={'ordering': ('-created_date',), 'verbose_name_plural': 'Meals'},
        ),
    ]
