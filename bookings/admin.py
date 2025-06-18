from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id', 'name', 'package_type', 'travel_month', 
        'nights', 'passengers', 'status', 'total_amount', 'created_at'
    )
    list_filter = (
        'status', 'package_type', 'travel_month', 'created_at', 
        'nights', 'passengers'
    )
    search_fields = (
        'booking_id', 'name', 'email', 'phone', 'package_type'
    )
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    list_editable = ('status',)
    list_per_page = 25
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'user', 'package', 'status')
        }),
        ('Customer Details', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Travel Details', {
            'fields': (
                'package_type', 'travel_month', 'nights', 'passengers',
                'departure_date', 'special_requirements'
            )
        }),
        ('Payment Information', {
            'fields': ('total_amount',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'package')
    
    def has_delete_permission(self, request, obj=None):
        # Only allow deletion of pending bookings
        if obj and obj.status in ['confirmed', 'completed']:
            return False
        return super().has_delete_permission(request, obj)
    
    actions = ['mark_as_confirmed', 'mark_as_cancelled', 'mark_as_completed']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} bookings marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} bookings marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected bookings as cancelled"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} bookings marked as completed.')
    mark_as_completed.short_description = "Mark selected bookings as completed"