from django.conf.urls import include, url
from .views import ServerAssetCreateView, ServerAssetListView

urlpatterns = [
    url(r'^$', ServerAssetListView.as_view()),
    url(r'^add/', ServerAssetCreateView.as_view())
]

