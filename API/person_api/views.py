# Create your views here.
from rest_framework import viewsets, generics, filters, mixins
from rest_framework.viewsets import GenericViewSet

from .models import University
from .serializers import UniversitySerializer


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all().order_by('id')
    serializer_class = UniversitySerializer


class UniversityAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericViewSet):
    search_fields = ['domains__domain']
    filter_backends = (filters.SearchFilter,)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
