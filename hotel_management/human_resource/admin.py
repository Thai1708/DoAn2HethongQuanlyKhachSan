from django.contrib import admin

from .models import Employee, Guest, User

admin.site.register(Employee)
admin.site.register(Guest)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'bio']

