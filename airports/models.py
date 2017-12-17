from django.db import models

# Include models

class Facility(models.Model):
    class Meta: app_label = "airports"    # Django needs a little help here

    # agency that supplied the data, e.g. 'FAA'
    agency_code = models.CharField(max_length=8)

    # ISO-3166 "Alpha-3" country codes (e.g. USA, CAN, MEX)
    # https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
    country_code = models.CharField(max_length=3)

    # Primary key of the facility with respect to the controlling agency.
    # FAA uses a "SiteNumber" in its database rather than the airport code.
    # e.g. SFO is assigned a SiteNumber of "01217.*A"
    agency_site_key = models.CharField(max_length=12, db_index=True)

    # local_id is the agency's airport code
    # e.g. LVK - Livermore
    local_id = models.CharField('Local Identifier', max_length=3, db_index=True)

    # Facility Type (e.g. AIRPORT, HELIPORT, SEAPORT, etc.)
    facility_type = models.CharField(max_length=12)

    # Effective date of the record (can generally be considered the last update date)
    effective_date = models.DateTimeField('Record Effective Date')

    # City where the facility is located
    city = models.CharField(max_length=64)

    # Name of the facility
    facility_name = models.CharField(max_length=64, null=True)

    # Elevation and elevation units of the facility (e.g. 400 FT)
    elevation = models.IntegerField(null=True)
    elevation_units = models.CharField(max_length=2, null=True)

    # Traffic Pattern Altitude of the facility (e.g. 400 FT) not as an altitude but
    # rather height above ground level (AGL)
    tpa_agl = models.IntegerField('Traffic Pattern Altitude (TPA), distance above ground (AGL)',
                                  null=True)
    tpa_agl_units = models.CharField('TPA (AGL) Units', max_length=2, null=True)

    # Magnetic Variation, degrees and direction (E or W), and year
    magnetic_variation_degrees = models.IntegerField(null=True)
    magnetic_variation_direction = models.CharField(max_length=2, null=True)
    magnetic_variation_year = models.IntegerField(null=True)

    # CTAF
    ctaf_frequency = models.DecimalField('Common Traffic Advisory Frequency (CTAF)',
                                         max_digits=6, decimal_places=3, null=True)

    # ICAO Airport Identifier (e.g. "KSFO", "CYEG")
    icao_id = models.CharField('ICAO Identifier', max_length=4, db_index=True, null=True)

    # Is public use?  Null means unknown.
    is_public_use = models.NullBooleanField()

    # Date the airport became active
    activation_date = models.DateField(null=True)

    # Latitude and Longitude in decimal degrees
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.local_id + ' (' + self.city + ')'


# Airport Runways

class Runway(models.Model):

    facility = models.ForeignKey('airports.Facility', related_name='runways', on_delete=models.CASCADE)

    # Primary key of the facility with respect to the controlling agency.
    # FAA uses a "SiteNumber" in its database rather than the airport code.
    # e.g. SFO is assigned a SiteNumber of "01217.*A"
    agency_site_key = models.CharField(max_length=12, db_index=True)

    runway_id = models.CharField(max_length=8)

    # Length and Length Units of the Runway
    runway_length = models.IntegerField(null=True)
    runway_length_units = models.CharField(max_length=2, null=True)

    # Width and Width Units of the Runway
    runway_width = models.IntegerField(null=True)
    runway_width_units = models.CharField(max_length=2, null=True)

    base_end_id = models.CharField(max_length=4)
    base_end_traffic_dir = models.CharField(max_length=1)

    reciprocal_end_id = models.CharField(max_length=4)
    reciprocal_end_traffic_dir = models.CharField(max_length=1)

    def __str__(self):
        return self.runway_id
