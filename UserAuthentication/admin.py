from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    fieldsets = (

        (None, {'fields': ('email', 'password',
         'fname', 'phone', 'board', 'grade', 'institute', 'websiteURL', 'instagramURL', 'facebookURL', 'telegramURL', 'youtubeURL',  'approved', 'room', 'last_login')}),
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
                'fields': ('email', 'password1', 'password2', 'fname', 'phone', 'board', 'grade', 'institute', 'room', 'websiteURL', 'instagramURL', 'facebookURL', 'telegramURL', 'youtubeURL')
            }
        ),
    )

    list_display = ('email', 'fname', 'phone', 'board', 'grade', 'institute', 'approved', 'room', 'last_login', 'websiteURL', 'instagramURL', 'youtubeURL', 'facebookURL', 'telegramURL')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    seach_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
