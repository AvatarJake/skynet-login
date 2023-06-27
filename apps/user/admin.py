from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, UserAccountManager

class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_online')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('username','first_name','last_name', 'fecha_nacimiento', 'dpi', 'fecha_contratacion', 'supervisor')}),
        ('Permisos', {'fields': ('is_superuser', 'is_staff', 'is_active','is_online', 'role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','username','first_name','last_name', 'fecha_nacimiento', 'dpi', 'fecha_contratacion', 'supervisor','is_staff', 'is_active', 'role'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(UserAccount, CustomUserAdmin)
