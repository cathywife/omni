from django.conf.urls import patterns, include, url
from .views import NodeAndGroupListView

urlpatterns = [
    url(r'^$|^index\.html$', NodeAndGroupListView.as_view()),
]
