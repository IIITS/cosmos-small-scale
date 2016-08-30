from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('btp.urls', namespace='btp')),
    url(r'^btp/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
]
handler404 = 'btp.views.page_not_found'
