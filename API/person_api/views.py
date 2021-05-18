# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, generics
from rest_framework.viewsets import GenericViewSet

from .models import University
from .serializers import UniversitySerializer


class UniversityViewSet(generics.ListAPIView, mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericViewSet,
                        ):
    filter_backends = [DjangoFilterBackend, ]
    queryset = University.objects.all().order_by('id')
    serializer_class = UniversitySerializer
    filterset_fields = ['country']
