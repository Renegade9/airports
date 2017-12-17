from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response

from django.contrib.auth.models import User
from airports.models import Facility

from rest_framework import generics, views, viewsets
from airports.serializers import UserSerializer, FacilitySerializer

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


class ListFacilities(generics.ListAPIView):
    """List Facilities with various filters"""
    #filter_backends = (filters.OrderingFilter,)
    #ordering_fields = ('name',)

    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()
