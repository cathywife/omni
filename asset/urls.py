from django.conf.urls import include, url

from apps.server import urls as server_url
urlpatterns = [
    url(r'server/', include(server_url)),
]
