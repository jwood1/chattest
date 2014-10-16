from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
# Enable the admin site
from django.contrib import admin
from views import auth, vlogout, index, register
from app import api
admin.autodiscover()


urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/favicon.ico')),

    url(r'^api', include(api.urls)),

    # log in, log out routes.
    url(r'^auth/?', auth, name='auth'),
    url(r'^logout/?', vlogout, name='logout'),
    url(r'^register/?', register, name='register'),

    # enable waffle urls
    (r'^', include('waffle.urls')),

    # Catch all, for history API routing
    url(r'^/?$', index, name='index')
)
