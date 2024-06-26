# Generated by Django 5.0.6 on 2024-05-29 15:31

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=255)),
                ('modified_by', models.CharField(default='admin', max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Floors',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('base_child', models.IntegerField(default=0)),
                ('bed_adult', models.IntegerField(default=0)),
                ('max_child', models.IntegerField(default=0)),
                ('max_adult', models.IntegerField(default=0)),
                ('description', models.TextField(default='')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=255)),
                ('modified_by', models.CharField(default='admin', max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Roomtypes',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_code', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('is_saled', models.BooleanField(default=True)),
                ('image', models.ImageField(default='images/default.png', upload_to='images/')),
                ('image1', models.ImageField(default='images/default.png', upload_to='images/')),
                ('image2', models.ImageField(default='images/default.png', upload_to='images/')),
                ('image3', models.ImageField(default='images/default.png', upload_to='images/')),
                ('bed_qty', models.IntegerField(default=0)),
                ('bath_qty', models.IntegerField(default=0)),
                ('description', models.TextField(default='')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=255)),
                ('modified_by', models.CharField(default='admin', max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('floor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='floor', to='store.floor')),
                ('room_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_type', to='store.roomtype')),
            ],
            options={
                'verbose_name_plural': 'Rooms',
                'ordering': ('-created_date',),
            },
            managers=[
                ('rooms', django.db.models.manager.Manager()),
            ],
        ),
    ]
