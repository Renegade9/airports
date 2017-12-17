from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response

from django.contrib.auth.models import User
from airports.models import Facility

from rest_framework import filters, generics, views, viewsets

from rest_framework.permissions import AllowAny
from airports.serializers import UserSerializer, FacilitySerializer

import django_filters

def index(request):
    return HttpResponse("Hello, world. You're at the airports index.")

def test(request):
    response = {'message': 'test JSON response'}
    return JsonResponse(response)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Facilities to be viewed or edited.
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class FindFacilityByCode(views.APIView):
    """Find a facility by code (FAA or ICAO airport code)"""
    permission_classes = (AllowAny,)

    def get(self, request, code):

        code = code.upper()

        # Lookup by the local code first
        facilities = Facility.objects.filter(local_id=code)
        if facilities.count() == 0:
            facilities = Facility.objects.filter(icao_id=code)

        if facilities.count() == 1:
            facility = facilities[0]
            serializer = FacilitySerializer(instance=facility)
            return Response(serializer.data)
        else:
            return JsonResponse({'status': 'error',
                                'message': 'Could not find: {}'.format(code)})


class CaseInsensitiveBooleanFilter(django_filters.Filter):
    """Agreed, we shouldn't have to do this"""

    def filter(self, qs, value):
        if value is not None:
            lc_value = value.lower()
            if lc_value in ('true', 'yes', 'y', 't', '1'):
                value = True
            elif lc_value in ('false', 'no', 'n', 'f', '0'):
                value = False
            return qs.filter(**{self.name: value})
        return qs


class FacilitiesFilter(django_filters.rest_framework.FilterSet):

    # use partial case insensitive filtering for city and facility name filters
    city = django_filters.CharFilter(name='city', lookup_expr='icontains')
    facility_name = django_filters.CharFilter(name='facility_name', lookup_expr='icontains')

    is_public_use = CaseInsensitiveBooleanFilter(name='is_public_use')
    state_or_prov = django_filters.CharFilter(name='state_or_prov')

    class Meta:
        model = Facility
        fields = ['city', 'facility_name', 'is_public_use', 'state_or_prov']


class FacilitiesList(generics.ListAPIView):
    """List Facilities with various filters"""
    permission_classes = (AllowAny,)

    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = ('local_id', 'icao_id', 'state_or_prov')
    filter_class = FacilitiesFilter

    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()
