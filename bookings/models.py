from django.db import models
from django.contrib.auth import get_user_model
from packages.models import Package
import uuid

User = get_user_model()

class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    
    # Customer details
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    # Booking details
    package_type = models.CharField(max_length=100, default="Standard")
    travel_month = models.CharField(max_length=50, default="January")
    nights = models.IntegerField(default=1)
    passengers = models.IntegerField(default=1)
    
    departure_date = models.DateField(null=True, blank=True)
    special_requirements = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_id} - {self.name}"

    def save(self, *args, **kwargs):
        # Auto-calculate total_amount if package is linked
        if self.package and self.passengers:
            self.total_amount = self.package.effective_price * self.passengers
        super().save(*args, **kwargs)
