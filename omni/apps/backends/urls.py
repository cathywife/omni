from django.conf.urls import include, url
from .views.saltstack import SaltStateView

urlpatterns = [
    url(r'^salt/state/$', SaltStateView.as_view()),
]
