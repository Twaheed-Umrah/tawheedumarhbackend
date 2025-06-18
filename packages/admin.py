from django.contrib import admin
from .models import Package

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_type', 'price', 'discounted_price', 'duration_days', 'is_featured', 'is_active')
    list_filter = ('package_type', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'discounted_price', 'is_featured', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'effective_price')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'package_type', 'short_description')
        }),
        ('Pricing', {
            'fields': ('price', 'discounted_price', 'effective_price')
        }),
        ('Package Details', {
            'fields': ('description', 'duration_days', 'max_passengers', 'image')
        }),
        ('Detailed Information', {
            'fields': ('includes', 'excludes', 'itinerary'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
