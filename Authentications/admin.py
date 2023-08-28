from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.



class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display = ('email', 'username' ,'is_staff','is_active',)
    list_filter = ('email', 'username','is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active' , 'is_claimAssure_admin','is_support_staff','is_document_manager','groups' , 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User , CustomUserAdmin)
