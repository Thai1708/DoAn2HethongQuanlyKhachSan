# Generated by Django 5.0.6 on 2024-06-11 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_alter_paymenttraninfor_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traninfor',
            name='booking_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traninfor_set', to='booking.bookinginfor'),
        ),
    ]
