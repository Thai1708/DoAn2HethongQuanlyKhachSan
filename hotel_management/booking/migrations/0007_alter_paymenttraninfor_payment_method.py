# Generated by Django 5.0.6 on 2024-06-07 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_paymenttraninfor_booking_infor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttraninfor',
            name='payment_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]