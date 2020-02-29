from api import views
from django.urls import re_path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'xxx', views.View1View)
urlpatterns = [
    # re_path(r'^api/v1/auth/$', views.AuthView.as_view()),
    # re_path(r'^api/v1/order/$', views.OrderView.as_view()),
    # re_path(r'^api/v1/info/$', views.UserInfo.as_view()),
    # re_path(r'^(?P<version>[v1|v2]+)/users/$', views.UsersView.as_view(), name="uuu"),
    # re_path(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view()),
    # re_path(r'^(?P<version>[v1|v2]+)/roles/$', views.RolesView.as_view()),
    # re_path(r'^(?P<version>[v1|v2]+)/userinfo/$', views.UserInfoView.as_view()),
    # re_path(r'^(?P<version>[v1|v2]+)/group/(?P<xxx>\dr+)$', views.GroupView.as_view(), name='gp'),
    # re_path(r'^(?P<version>[v1|v2]+)/usergroup/$', views.UserGroupView.as_view(), name='gp'),
    # re_path(r'^(?P<version>[v1|v2]+)/page1/$', views.PageView.as_view()),
    # re_path(r'^(?P<version>[v1|v2]+)/v1/$', views.View1View.as_view({'get': 'list', 'post': 'create'})),
    # re_path(r'^(?P<version>[v1|v2]+)/v1/(?P<pk>\d+)/$', views.View1View.as_view(
    #     {'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
    re_path(r'^(?P<vesion>[v1|v2]+)/', include(router.urls)),
]
