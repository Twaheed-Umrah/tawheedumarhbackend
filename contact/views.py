from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ContactUs
from authentication.permissions import IsConsultingOrAbove
from .serializers import ContactUsSerializer

class ContactUsCreateView(generics.CreateAPIView):
    serializer_class = ContactUsSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Thank you for contacting  us. We will get back to you soon.'
        }, status=status.HTTP_201_CREATED)

class ContactUsListView(generics.ListAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsConsultingOrAbove]

