from django.contrib import admin
from .models import ContactUs

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'package_type', 'is_processed', 'created_at')
    list_filter = ('package_type', 'is_processed', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('package_type', 'message')
        }),
        ('Status', {
            'fields': ('is_processed', 'created_at')
        })
    )
