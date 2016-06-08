from django.conf.urls import include, url
from .apps.backends import urls as omni_backends_urls
from .apps.host_node import urls as omni_host_urls
from djcelery import urls as djcelery_urls
from asset import urls as asset_urls

from . import views as omni_view

urlpatterns = [
    url(r'^$|^index\.html$', omni_view.index),
    url(r'^login\.html$', omni_view.login),
    url(r'^logout\.htm$', omni_view.logout),
]

urlpatterns += [
    url(r'^backends/', include(omni_backends_urls))
]

urlpatterns += [
    url(r'^asset/', include(asset_urls))
]

urlpatterns += [
    url(r'^host/', include(omni_host_urls))
]

urlpatterns += [
    url(r'^celery/', include(djcelery_urls))
]
