from django.db import models

class ContactUs(models.Model):
    # Contact us form data
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    package_type = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return f"Contact - {self.name} "
