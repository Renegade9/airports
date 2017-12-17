from django.contrib import admin

# Register your models here.
from airports.models import Facility

# Make our model available via Django admin interface
admin.site.register(Facility)
