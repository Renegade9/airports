from django.contrib.auth.models import User, Group
from airports.models import Facility, Runway

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class RunwaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Runway
        fields = ('runway_id', 'runway_length', 'runway_length_units',
                  'runway_width', 'runway_width_units',
                  'base_end_id', 'base_end_traffic_dir',
                  'reciprocal_end_id', 'reciprocal_end_traffic_dir',
                  )

class FacilitySerializer(serializers.HyperlinkedModelSerializer):

    skyvector_url = serializers.SerializerMethodField()

    def get_skyvector_url(self, obj):
        return 'https://skyvector.com/?ll={},{}&chart=301&zoom=1&fpl={}'.format(
            obj.latitude, obj.longitude, obj.icao_id
        )

    runways = RunwaySerializer(read_only=True, many=True)

    class Meta:
        model = Facility
        fields = ('agency_code', 'country_code', 'state_or_prov', 'local_id', 'facility_type', 'city',
                  'facility_name', 'elevation', 'elevation_units', 'tpa_agl', 'tpa_agl_units',
                  'magnetic_variation_degrees', 'magnetic_variation_direction',
                  'magnetic_variation_year', 'ctaf_frequency', 'is_public_use',
                  'activation_date', 'icao_id', 'latitude', 'longitude', 'skyvector_url',
                  'runways')
