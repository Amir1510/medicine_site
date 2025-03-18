from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from medicine_app.models import CreateUser

class CreateUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )

admin.site.register(CreateUser, CreateUserAdmin)