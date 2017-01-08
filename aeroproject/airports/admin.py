from django.contrib import admin

# Register your models here.
from model_definitions import Facility

# Make our model available via Django admin interface
admin.site.register(Facility)