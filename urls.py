from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^search', 'childsearch.views.checkPY', name='home'),
    url(r'^$', 'childsearch.views.default', name='home'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    ('^admin/',include(admin.site.urls)),
    

 
    # Examples:
    # url(r'^$', 'childsearch.views.home', name='home'),
    # url(r'^childsearch/', include('childsearch.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', inclsude('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
