from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from accounts.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('last_name', 'first_name', 'email', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        ('Informacje personalne', {'fields': ('email', 'first_name', 'last_name', 'mobile_nr', 'pesel', 'holiday_allowance')}),
        ('Uprawnienia', {'fields': ('is_admin','is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'mobile_nr', 'pesel', 'holiday_allowance'),
        }),
    )
    search_fields = ('last_name',)
    ordering = ('last_name',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(get_user_model(), UserAdmin)
