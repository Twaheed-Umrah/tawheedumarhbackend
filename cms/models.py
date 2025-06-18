
# models.py
from django.db import models

class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    background_video = models.FileField(upload_to='hero_videos/', blank=True, null=True)
    background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Component(models.Model):
    COMPONENT_TYPES = [
        ('about', 'About Section'),
        ('services', 'Services Section'),
        ('testimonials', 'Testimonials'),
        ('gallery', 'Gallery'),
        ('features', 'Features'),
    ]
    
    name = models.CharField(max_length=100)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='component_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.component_type}"

class Package(models.Model):
    PACKAGE_TYPES = [
        ('umrah_classic', 'Classic Umrah Package'),
        ('umrah_delux', 'Delux Umrah Package'),
        ('umrah_luxury', 'Luxury Umrah Package'),
        ('hajj_classic', 'Classic Hajj Package'),
        ('hajj_delux', 'Delux Hajj Package'),
        ('hajj_luxury', 'Luxury Hajj Package'),
        ('ramadan_early', 'Early Ramadan Package'),
        ('ramadan_laylat', 'Laylat al-Qadr Package'),
        ('ramadan_full', 'Full Month Ramadan Package'),
    ]
    
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    image = models.ImageField(upload_to='package_images/', blank=True, null=True)
    features = models.TextField(help_text="Enter features separated by new lines", blank=True)
    duration_days = models.IntegerField(default=7)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['package_type']

    def __str__(self):
        return self.title

    def get_features_list(self):
        """Return features as a list"""
        return [feature.strip() for feature in self.features.split('\n') if feature.strip()]

class HomePage(models.Model):
    content = models.TextField(help_text="Main content for the homepage")
    background_video = models.FileField(upload_to='homepage_videos/', blank=True, null=True)
    background_image = models.ImageField(upload_to='homepage_images/', blank=True, null=True)
    welcome_title = models.CharField(max_length=200, default="Welcome")
    welcome_subtitle = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Homepage Content - {self.welcome_title}"