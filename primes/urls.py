from django.conf.urls import patterns, include, url
from django.contrib import admin

from generation import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^get_prime$', views.get_prime, name="get_prime"),
    url(r'^primes$', views.primes, name="primes"),
    url(r'^admin/', include(admin.site.urls)),
)
