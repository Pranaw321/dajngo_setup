from django.contrib import admin
from .models import ExtUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = ExtUser
    search_fields = ('mobile_no', 'email', 'first_name','last_name')
    list_filter = ('mobile_no', 'email', 'first_name', 'last_name', 'is_active','is_staff')
    ordering = ('-joining_date',)
    list_display = ('email', 'mobile_no', 'first_name', 'last_name',
                    'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'is_email_verified' , 'mobile_no', 'is_mobile_no_verified', 'first_name', 'last_name','address', 'permissions')}),        
        ('Permissions', {'fields': ('is_staff','is_active',)}),
    )
    # formfield_overrides = {
    #     ExtUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    # }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_no', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active','is_staff', 'user_permissions', 'groups')}
         ),
    )
admin.site.register(ExtUser, UserAdminConfig)