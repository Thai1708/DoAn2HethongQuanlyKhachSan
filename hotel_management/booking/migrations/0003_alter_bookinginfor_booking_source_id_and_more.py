# Generated by Django 5.0.6 on 2024-06-05 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_initial'),
        ('human_resource', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinginfor',
            name='booking_source_id',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.bookingsource'),
        ),
        migrations.AlterField(
            model_name='bookinginfor',
            name='saleman_id',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='human_resource.employee'),
        ),
        migrations.AlterField(
            model_name='rentalinfor',
            name='charges',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.charges'),
        ),
        migrations.AlterField(
            model_name='rentalinfor',
            name='rental_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='traninfor',
            name='cancel_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='traninfor',
            name='checkin_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='traninfor',
            name='checkout_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
