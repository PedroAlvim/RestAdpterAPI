# Create your views here.
from rest_framework import viewsets, generics, filters

from .models import University
from .serializers import UniversitySerializer


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all().order_by('id')
    serializer_class = UniversitySerializer


class UniversityAPIView(generics.ListCreateAPIView):
    search_fields = ['domains__domain']
    filter_backends = (filters.SearchFilter,)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
