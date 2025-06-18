# views.py
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import HeroSection, Component, Package, HomePage
from .serializers import (
    HeroSectionSerializer, ComponentSerializer, PackageSerializer, 
    PackageUpdateSerializer, HomePageSerializer, HomePageUpdateSerializer
)
# Import your custom permissions
from authentication.permissions import IsAdminOrSuperAdmin

class HeroSectionListView(generics.ListAPIView):
    serializer_class = HeroSectionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return HeroSection.objects.filter(is_active=True)

class HeroSectionUpdateView(generics.RetrieveUpdateAPIView):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    permission_classes = [IsAdminOrSuperAdmin]  # Changed from permissions.IsAdminUser

class ComponentListView(generics.ListAPIView):
    serializer_class = ComponentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        component_type = self.request.query_params.get('type', None)
        queryset = Component.objects.filter(is_active=True)
        if component_type:
            queryset = queryset.filter(component_type=component_type)
        return queryset

class ComponentUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [IsAdminOrSuperAdmin]  # Changed from permissions.IsAdminUser

# Package Views
class PackageListView(generics.ListAPIView):
    serializer_class = PackageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        package_type = self.request.query_params.get('type', None)
        queryset = Package.objects.filter(is_active=True)
        if package_type:
            queryset = queryset.filter(package_type=package_type)
        return queryset

class PackageDetailView(generics.RetrieveAPIView):
    serializer_class = PackageSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'package_type'

    def get_queryset(self):
        return Package.objects.filter(is_active=True)

class PackageUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageUpdateSerializer
    permission_classes = [IsAdminOrSuperAdmin]  # Changed from permissions.IsAdminUser
    lookup_field = 'package_type'

# NEW: Package Create View
class PackageCreateView(generics.CreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAdminOrSuperAdmin]  # Changed from permissions.IsAdminUser

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_packages_by_category(request):
    """Get packages grouped  by  category"""
    umrah_packages = Package.objects.filter(
        package_type__startswith='umrah_', is_active=True
    ).order_by('package_type')
    
    hajj_packages = Package.objects.filter(
        package_type__startswith='hajj_', is_active=True
    ).order_by('package_type')
    
    ramadan_packages = Package.objects.filter(
        package_type__startswith='ramadan_', is_active=True
    ).order_by('package_type')
    
    data = {
        'umrah_packages': PackageSerializer(umrah_packages, many=True).data,
        'hajj_packages': PackageSerializer(hajj_packages, many=True).data,
        'ramadan_packages': PackageSerializer(ramadan_packages, many=True).data,
    }
    
    return Response(data)

@api_view(['PATCH'])
@permission_classes([IsAdminOrSuperAdmin])  # Changed from permissions.IsAdminUser
def update_package_price(request, package_type):
    """Update only the price of a  specific package"""
    package = get_object_or_404(Package, package_type=package_type)
    
    if 'price' in request.data:
        package.price = request.data['price']
        package.save()
        return Response({
            'message': 'Package price updated successfully',
            'package_type': package_type,
            'new_price': package.price
        })
    else:
        return Response({'error': 'Price field is required'}, status=status.HTTP_400_BAD_REQUEST)

# NEW: Create Package Function
@api_view(['POST'])
@permission_classes([IsAdminOrSuperAdmin])  # Changed from permissions.IsAdminUser
def create_package(request):
    """Create a new package"""
    serializer = PackageSerializer(data=request.data)
    if serializer.is_valid():
        package = serializer.save()
        return Response({
            'message': 'Package created successfully',
            'package': PackageSerializer(package).data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            'error': 'Failed to create package',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# Homepage Views
# Homepage Views - FIXED
class HomePageView(generics.ListAPIView):
    serializer_class = HomePageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return HomePage.objects.filter(is_active=True)
    
    def get_serializer_context(self):
        """Pass request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class HomePageUpdateView(generics.RetrieveUpdateAPIView):
    queryset = HomePage.objects.all()
    serializer_class = HomePageUpdateSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get_serializer_context(self):
        """Pass request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class HomePageCreateView(generics.CreateAPIView):
    queryset = HomePage.objects.all()
    serializer_class = HomePageSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get_serializer_context(self):
        """Pass request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_active_homepage(request):
    """Get the active homepage content"""
    try:
        homepage = HomePage.objects.filter(is_active=True).first()
        if homepage:
            # FIXED: Pass request context to serializer
            serializer = HomePageSerializer(homepage, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'message': 'No active homepage content found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAdminOrSuperAdmin])
def create_homepage(request):
    """Create a new homepage content"""
    # FIXED: Pass request context to serializer
    serializer = HomePageSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        homepage = serializer.save()
        # Also pass context when returning the response
        response_serializer = HomePageSerializer(homepage, context={'request': request})
        return Response({
            'message': 'Homepage content created successfully',
            'homepage': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            'error': 'Failed to create homepage content',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_packages(request):
    """Get all active packages - public access"""
    try:
        packages = Package.objects.filter(is_active=True).order_by('id')
        serializer = PackageSerializer(packages, many=True)
        return Response({
            'success': True,
            'count': packages.count(),
            'packages': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    