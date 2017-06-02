from django.conf.urls import include, url
from .views import hostgroup, swimlane, cluster, product


urlpatterns = [
    url(r'^hostgroup$|^hostgroup/+index\.html$', hostgroup.HostGroupView.as_view()),
    url(r'^hostgroup/+search/+?$', hostgroup.HostGroupSearchView.as_view()),
    url(r'^hostgroup/+appid/+?$', hostgroup.HostGroupInfoAppIdView.as_view()),
    url(r'^hostgroup/+host/+?$', hostgroup.HostGroupInfoHostsView.as_view()),
    url(r'^hostgroup/+appid/+add/+?$', hostgroup.HostGroupAddAppidView.as_view()),
    url(r'^hostgroup/+host/+add/+?$', hostgroup.HostGroupAddHostsView.as_view()),
    url(r'^hostgroup/+appid/+del/+?$', hostgroup.HostGroupDelAppidView.as_view()),
    url(r'^hostgroup/+host/+del/+?$', hostgroup.HostGroupDelHostsView.as_view()),

    url(r'^products/+create/+$', product.ProductCreateTemplateView.as_view(), name='product-create'),
    url(r'^products/+$', product.ProductCreateTemplateView.as_view(), name='product-list'),
    url(r'^products/+(?P<pk>\d+)/+$', product.ProductDetailAPIView.as_view(), name='product-detail'),

    url(r'^projects/+create/+$', product.ProjectCreateTemplateView.as_view(), name='project-create'),
    url(r'^projects/+$', product.ProductCreateTemplateView.as_view(), name='project-list'),
    url(r'^projects/+(?P<pk>\d+)/+$', product.ProjectDetailAPIView.as_view(), name='project-detail'),

    url(r'^appids/+$', product.AppIdListTemplateView.as_view(), name='appid-list'),
    url(r'^appids/+(?P<pk>\d+)/+update/+$', product.AppIdUpdateTemplateView.as_view(), name='appid-update'),
    url(r'^appids/+(?P<pk>\d+)/+', product.AppIdDetailTemplateView.as_view(), name='appid-detail'),

    url(r'^clusters/+templates/+create/+$', cluster.ClusterTemplateCreateTemplateView.as_view(),
        name='cluster-template-create'),
    url(r'^clusters/+templates/+(?P<pk>\d+)/+$', cluster.ClusterTemplateDetailTemplateView.as_view(),
        name='cluster-template-detail'),
    url(r'clusters/+templates/+(?P<cluster_template_id>\d+)/+versions/create/+$',
        cluster.ClusterTemplateVersionCreateTemplateView.as_view(), name='cluster-template-version-create'),
    url(r'clusters/+templates/+(?P<cluster_template_id>\d+)/+versions/+(?P<version>\d+)/+$',
        cluster.ClusterTemplateVersionDetailTemplateView.as_view(), name='cluster-template-version-detail'),
    url(r'^clusters/+templates/+$', cluster.ClusterTemplateListTemplateView.as_view(),
        name='cluster-template-list'),

]
