from django.conf.urls import patterns, include, url

from cmc.apps.env import urls as env_urls

urlpatterns = patterns(
    '',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^env/', include(env_urls)),
)