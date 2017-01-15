from __future__ import unicode_literals

from django.db import models

# Airport Runways

class Runway(models.Model):

    facility = models.ForeignKey('airports.Facility')

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

    def __str__(self):
        return self.runway_id
