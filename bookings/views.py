from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from authentication.permissions import IsConsultingOrAbove
from .models import Booking
from .serializers import (
    BookingSerializer, BookingTrackingSerializer, BookingListSerializer,BookingStatusUpdateSerializer
)

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        return Response({
            'success': True,
            'message': 'Booking created successfully',
            'booking_id': str(booking.booking_id),
            'booking': BookingTrackingSerializer(booking).data
        }, status=status.HTTP_201_CREATED)

class BookingListView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def track_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    serializer = BookingTrackingSerializer(booking)
    return Response({
        'success': True,
        'booking': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def booking_detail(request, booking_id):
    """Get detailed booking information"""
    try:
        booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        serializer = BookingTrackingSerializer(booking)
        return Response(serializer.data)
    except Booking.DoesNotExist:
        return Response(
            {'error': 'Booking not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_booking(request, booking_id):
    """Update booking details"""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    if booking.status != 'pending':
        return Response({
            'error': 'Cannot update booking that is not pending'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = BookingSerializer(booking, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Booking updated successfully',
            'booking': BookingTrackingSerializer(booking).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    if booking.status == 'completed':
        return Response({
            'error': 'Cannot cancel completed booking'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    booking.status = 'cancelled'
    booking.save()

    return Response({
        'success': True,
        'message': 'Booking cancelled successfully'
    })

class AdminBookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingTrackingSerializer
    permission_classes = [IsConsultingOrAbove]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Add filtering options
        status_param = self.request.query_params.get('status')
        package_type = self.request.query_params.get('package_type')
        travel_month = self.request.query_params.get('travel_month')
        
        if status_param:
            queryset = queryset.filter(status=status_param)
        if package_type:
            queryset = queryset.filter(package_type__icontains=package_type)
        if travel_month:
            queryset = queryset.filter(travel_month__icontains=travel_month)
        
        return queryset

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsConsultingOrAbove])
def admin_booking_detail(request, booking_id):
    """Admin: Get detailed booking information by booking_id"""
    booking = get_object_or_404(Booking, booking_id=booking_id)
    serializer = BookingTrackingSerializer(booking)
    return Response({
        'success': True,
        'booking': serializer.data
    })

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated, IsConsultingOrAbove])
def admin_update_booking(request, booking_id):
    """Admin: Update booking status only"""
    print("Request method:", request.method)
    print("Request data:", request.data)
    print("Request POST:", request.POST)
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    new_status = request.data.get('status')
    valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
    
    if not new_status:
        return Response({
            'error': 'Status field is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if new_status not in valid_statuses:
        return Response({
            'error': 'Invalid status value'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    booking.status = new_status
    booking.save()
    
    return Response({
        'success': True,
        'message': f'Booking status updated to {new_status}',
        'booking': BookingTrackingSerializer(booking).data
    })

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, IsConsultingOrAbove])
def admin_cancel_booking(request, booking_id):
    """Admin: Cancel any booking"""
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if booking.status == 'completed':
        return Response({
            'error': 'Cannot cancel completed booking'
        }, status=status.HTTP_400_BAD_REQUEST)

    booking.status = 'cancelled'
    booking.save()

    return Response({
        'success': True,
        'message': 'Booking cancelled successfully'
    })