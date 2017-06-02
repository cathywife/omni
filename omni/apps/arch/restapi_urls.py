from django.conf.urls import include, url
from .views import hostgroup, swimlane, cluster, product, host


urlpatterns = [
    url(r'^products/+$', product.ProductListCreateAPIView.as_view(), name='product-list_create'),
    url(r'^products/+(?P<pk>\d+)/+$', product.ProductDetailAPIView.as_view(), name='product-detail'),

    url(r'^projects/+$', product.ProjectListCreateAPIView.as_view(), name='project-list_create'),
    url(r'^projects/+(?P<pk>\d+)/+$', product.ProjectDetailAPIView.as_view(), name='project-detail'),

    url(r'host/+models/+$', host.HostModelListAPIView.as_view(), name='host-model-list'),

    url(r'^appids/+sync-all/+$', product.AppIdInfoUpdateAPIView.as_view(), name='appid-sync_all'),
    url(r'^appids/+$', product.AppIdListAPIView.as_view(), name='appid-list'),
    url(r'^appids/+(?P<pk>\d+)/+$', product.AppIdDetailAPIView.as_view(), name='appid-detail'),

    url(r'^swimlanes/+$', swimlane.SwimlaneListAPIView.as_view(), name='swimlanes-list'),

    url(r'^clusters/+templates/+$', cluster.ClusterTemplateListCreateAPIView.as_view(),
        name='cluster-template-list_create'),
    url(r'^clusters/+templates/+(?P<pk>\d+)/+$', cluster.ClusterTemplateDetailAPIView.as_view(),
        name='cluster-template-detail'),
    url(r'^clusters/+templates/+(?P<cluster_template_id>\d+)/+versions/+$',
        cluster.ClusterTemplateVersionListCreateAPIView.as_view(), name='cluster-template-version-list_create'),
    url(r'^clusters/+templates/+(?P<cluster_template_id>\d+)/+versions/+(?P<version>\d+)/+',
        cluster.ClusterTemplateVersionDetailAPIView.as_view(), name='cluster-template-version-detail')

]
