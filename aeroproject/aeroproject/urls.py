# aeroproject Top-level URL Configuration

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^airports/', include('airports.urls')),
]
