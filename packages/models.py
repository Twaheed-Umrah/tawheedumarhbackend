from django.db import models

class Package(models.Model):
    PACKAGE_TYPES = [
        ('hajj', 'Hajj'),
        ('umrah', 'Umrah'),
        ('ramadan', 'Ramadan Special'),
    ]
    
    name = models.CharField(max_length=200)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration_days = models.IntegerField()
    max_passengers = models.IntegerField()
    image = models.ImageField(upload_to='package_images/')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Package details
    includes = models.TextField(help_text="What's included in the package")
    excludes = models.TextField(help_text="What's not included", blank=True)
    itinerary = models.TextField(help_text="Day-wise itinerary", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_package_type_display()}"

    @property
    def effective_price(self):
        return self.discounted_price if self.discounted_price else self.price
