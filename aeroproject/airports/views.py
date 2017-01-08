from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User
from model_definitions import Facility

from rest_framework import viewsets
from serializers import UserSerializer, FacilitySerializer

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