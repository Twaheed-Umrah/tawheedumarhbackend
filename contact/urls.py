# ==================== contact/urls.py ====================
from django.urls import path
from .views import ContactUsCreateView, ContactUsListView

urlpatterns = [
    path('', ContactUsCreateView.as_view(), name='contact-us'),
    path('list/', ContactUsListView.as_view(), name='contact-us-list'),
]