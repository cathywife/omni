from django.conf.urls import include, url

from .apps.arch import urls as omni_arch_urls
from .apps.cmc import urls as omni_cmc_urls

from . import views as omni_view
from omni.libs.django.view.common import MatchByUrlTemplateView

urlpatterns = [
    url(r'^$|^/*index\.html$', omni_view.index),
    url(r'^/*login\.html$', omni_view.login),
    url(r'^/*logout\.htm$', omni_view.logout),
]

# arch for restful api
urlpatterns += [
    url(r'^/*restapi/+arch/+', include('omni.apps.arch.restapi_urls', namespace='restapi-arch', app_name='arch')),
    url(r'^/*restapi/+cmc/+', include('omni.apps.cmc.restapi_urls', namespace='restapi-cmc', app_name='cmc')),

    url(r'^/*arch/+', include('omni.apps.arch.urls', namespace='template-arch', app_name='arch')),
    url(r'^/*cmc/+', include('omni.apps.cmc.urls', namespace='template-cmc', app_name='cmc')),
]
