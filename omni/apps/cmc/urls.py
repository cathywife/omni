from django.conf.urls import include, url
from .views import user


urlpatterns = [
    url(r'^users/+create/+$', user.UserInfoCreateTemplateView.as_view()),
    url(r'^usergroups/+create/+$', user.UserGroupCreateTemplateView.as_view()),
    url(r'^departments/+create/+$', user.UserDepartmentCreateTemplateView.as_view()),
    url(r'^departments/+(?P<pk>\d+)/+', user.UserDepartmentDetailTemplateView.as_view(), name='department-detail')

]