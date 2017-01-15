from django.contrib.auth.models import User, Group
from model_definitions import Facility

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class FacilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Facility
        fields = ('agency_code', 'country_code', 'local_id', 'facility_type', 'city',
                  'facility_name', 'elevation', 'elevation_units', 'tpa_agl', 'tpa_agl_units',
                  'magnetic_variation_degrees', 'magnetic_variation_direction',
                  'magnetic_variation_year', 'ctaf_frequency', 'is_public_use',
                  'activation_date', 'icao_id')
