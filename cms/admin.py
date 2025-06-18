# admin.py
from django.contrib import admin
from .models import HeroSection, Component, Package, HomePage


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle')
        }),
        ('Media', {
            'fields': ('background_video', 'background_image')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_type', 'title', 'is_active', 'order')
    list_filter = ('component_type', 'is_active', 'created_at')
    search_fields = ('name', 'title', 'description')
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'component_type', 'title')
        }),
        ('Content', {
            'fields': ('description', 'image')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'package_type', 'price', 'currency', 'duration_days', 'is_active', 'is_featured')
    list_filter = ('package_type', 'is_active', 'is_featured', 'currency', 'created_at')
    search_fields = ('title', 'description', 'package_type')
    list_editable = ('price', 'is_active', 'is_featured')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('package_type', 'title', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'currency', 'duration_days')
        }),
        ('Content', {
            'fields': ('image', 'features')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('welcome_title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('welcome_title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('welcome_title', 'welcome_subtitle', 'content')
        }),
        ('Media', {
            'fields': ('background_video', 'background_image')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )