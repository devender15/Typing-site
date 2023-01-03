from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    fieldsets = (

        (None, {'fields': ('email', 'password',
         'fname', 'phone', 'board', 'grade', 'institute', 'website_url', 'instagram_url', 'facebook_url', 'telegram_url', 'youtube_url',  'approved', 'room', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'fname', 'phone', 'board', 'grade', 'institute', 'room', 'website_url', 'instagram_url', 'facebook_url', 'telegram_url', 'youtube_url')
            }
        ),
    )

    list_display = ('email', 'fname', 'phone', 'board', 'grade', 'institute', 'approved', 'room', 'last_login', 'website_url', 'instagram_url', 'youtube_url', 'facebook_url', 'telegram_url')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    seach_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
