# ==================== bookings/urls.py ====================
from django.urls import path
from .views import (
    BookingCreateView, BookingListView, track_booking, booking_detail,
    update_booking, cancel_booking, AdminBookingListView ,admin_booking_detail,admin_update_booking,admin_cancel_booking,
)

urlpatterns = [
    # User booking endpoints
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('my-bookings/', BookingListView.as_view(), name='my-bookings'),
    path('track/<uuid:booking_id>/', track_booking, name='track-booking'),
    path('detail/<uuid:booking_id>/', booking_detail, name='booking-detail'),
    path('update/<uuid:booking_id>/', update_booking, name='update-booking'),
    path('cancel/<uuid:booking_id>/', cancel_booking, name='cancel-booking'),
    
    # Admin endpoints
    path('admin/bookings/', AdminBookingListView.as_view(), name='admin-booking-list'),
      path('admin/bookings-details/<uuid:booking_id>/', admin_booking_detail, name='admin-booking-details'),
      path('admin/bookings/update/<uuid:booking_id>/', admin_update_booking, name='admin-update-booking'),
    path('admin/bookings/cancel/<uuid:booking_id>/', admin_cancel_booking, name='admin-cancel-booking'),
]