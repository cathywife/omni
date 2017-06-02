from django.conf.urls import include, url
from .views import user

urlpatterns = [
    url(r'^users/+$', user.UserListCreateAPIView.as_view(), name='user-list_create'),
    url(r'^users/+(?P<pk>\d+)/+$', user.UserDetailAPIView.as_view(), name='user-detail'),

    url(r'^usergroups/+$', user.UserGroupListCreateAPIView.as_view(), name='usergroup-list_create'),
    url(r'^usergroups/+(?P<pk>\d+)/+', user.UserGroupDetailAPIView.as_view(), name='usergroup-detail'),

    url(r'^departments/+$', user.UserDepartmentListCreateAPIView.as_view(), name='department-list_create'),
    url(r'^departments/+(?P<pk>\d+)/+$', user.UserDepartmentDetailAPIView.as_view(), name='department-detail'),
]
