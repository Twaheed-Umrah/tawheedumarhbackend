from django.urls import path
from .views import (
    HeroSectionListView, HeroSectionUpdateView,
    ComponentListView, ComponentUpdateView,
    PackageListView, PackageDetailView, PackageUpdateView, PackageCreateView,
    HomePageView, HomePageUpdateView, HomePageCreateView,
    get_packages_by_category, update_package_price, get_active_homepage,
    create_package, create_homepage,get_all_packages
)

urlpatterns = [
    # Hero Section URLs
    path('hero-section/', HeroSectionListView.as_view(), name='hero-section-list'),
    path('hero-section/<int:pk>/', HeroSectionUpdateView.as_view(), name='hero-section-update'),
    
    # Component URLs
    path('components/', ComponentListView.as_view(), name='component-list'),
    path('components/<int:pk>/', ComponentUpdateView.as_view(), name='component-update'),
    
    # Package URLs
    path('packages/', PackageListView.as_view(), name='package-list'),
    path('packages/create/', PackageCreateView.as_view(), name='package-create'),  # NEW
    path('packages/add/', create_package, name='package-add'),  # NEW Function-based
    path('packages/categories/', get_packages_by_category, name='packages-by-category'),
    path('packages/<str:package_type>/', PackageDetailView.as_view(), name='package-detail'),
    path('packages/<str:package_type>/update/', PackageUpdateView.as_view(), name='package-update'),
    path('packages/<str:package_type>/price/', update_package_price, name='package-price-update'),
    
    # Homepage URLs
    path('homepage/', HomePageView.as_view(), name='homepage-list'),
    path('homepage/create/', HomePageCreateView.as_view(), name='homepage-create'),  # NEW
    path('homepage/add/', create_homepage, name='homepage-add'),  # NEW Function-based
    path('homepage/active/', get_active_homepage, name='homepage-active'),
    path('homepage/<int:pk>/', HomePageUpdateView.as_view(), name='homepage-update'),
    path('packages/all/', get_all_packages, name='all-packages'), 
]