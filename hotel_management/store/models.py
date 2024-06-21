from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class RoomManager(models.Manager):
    def get_queryset(self):
        return super(RoomManager, self).get_queryset().filter(is_saled=True)
    
class RoomType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    base_child = models.IntegerField(default=0)
    bed_adult = models.IntegerField(default=0)
    max_child = models.IntegerField(default=0)
    max_adult = models.IntegerField(default=0)
    description = models.TextField(default='')  # Cung cấp giá trị mặc định là chuỗi rỗng
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='admin')
    modified_by = models.CharField(max_length=255, default='admin')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Roomtypes'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class Floor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='admin')
    modified_by = models.CharField(max_length=255, default='admin')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Floors'

    def __str__(self):
        return self.name

class Room(models.Model):
    room_code = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    room_type_id = models.ForeignKey(RoomType, related_name='room_type', on_delete=models.SET_NULL, null=True)
    floor_id = models.ForeignKey(Floor, related_name='floor', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_saled = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    image1 = models.ImageField(upload_to='images/', default='images/default.png')
    image2 = models.ImageField(upload_to='images/', default='images/default.png')
    image3 = models.ImageField(upload_to='images/', default='images/default.png')
    bed_qty = models.IntegerField(default=0)
    bath_qty = models.IntegerField(default=0)
    description = models.TextField(default='')  # Cung cấp giá trị mặc định là chuỗi rỗng
    rooms = RoomManager()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, default='admin')
    modified_by = models.CharField(max_length=255, default='admin')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Rooms'
        ordering = ('-created_date',)

    def get_absolute_url(self):
        return reverse('store:room_detail', args=[self.slug])

    def __str__(self):
        return self.room_code
