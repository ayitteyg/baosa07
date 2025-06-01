

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import CustomUser, Member, AnnualDues
from import_export.admin import ImportExportModelAdmin, ExportMixin, ImportMixin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_executive', 'is_staff']

    # Add is_executive to the regular (edit) form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_executive',)}),
    )

    # Add is_executive to the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_executive',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'category', 'location', 'date_joined')
    search_fields = ('name', 'contact', 'location', 'work')
    list_filter = ('category', 'marital_status', 'location')



@admin.register(AnnualDues)
class AnnualDuesAdmin(admin.ModelAdmin):
    pass