# ====================/packages/urls.py ====================
from django.urls import path
from .views import PackageListView, PackageDetailView, PackageUpdateView

urlpatterns = [
    path('', PackageListView.as_view(), name='package-list'),
    path('<int:pk>/', PackageDetailView.as_view(), name='package-detail'),
    path('<int:pk>/update/', PackageUpdateView.as_view(), name='package-update'),
]