from django.contrib import admin
from .models import myUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = myUser
    search_fields = ('email', 'username', 'first_name',)
    list_filter = ('email', 'username', 'first_name','is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('id','email', 'username', 'first_name','middle_name','last_name', 'phone_number','address',
                    'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name','last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2','phone_number', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(myUser, UserAdminConfig)