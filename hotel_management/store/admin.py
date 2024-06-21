from django.contrib import admin
from .models import Room, RoomType, Floor

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('room_code',)}

admin.site.register(Floor)
