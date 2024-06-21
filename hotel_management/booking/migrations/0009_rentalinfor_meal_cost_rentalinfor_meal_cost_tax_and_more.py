# Generated by Django 5.0.6 on 2024-06-11 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_alter_traninfor_booking_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalinfor',
            name='meal_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='rentalinfor',
            name='meal_cost_tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='rentalinfor',
            name='meal_cost_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]