"""
URL configuration for customer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve as static_serve

from bbs import views, account, index, down, dxf

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path('currentversion/<int:nid>/delete/', dxf.current_version_delete),
    path('currentversion/<int:nid>/edit/', dxf.current_version_edit),
    path('currentversion/add/', dxf.current_version_add),
    path('currentversion/list/', dxf.current_version_list),
    path('memberrecord/list/', dxf.member_record_list),
    path('membermodel/<int:nid>/edit/', dxf.member_model_edit),
    path('membermodel/list/', dxf.member_model_list),
    path('usermanager/add/', dxf.user_add),
    path('usermanager/<int:nid>/edit/', dxf.user_edit),
    path('usermanager/list/', dxf.user_list),
    path('index/download_file/', down.download_file),
    path('index/pay_result/', index.pay_result),
    path('index/pay/', index.pay),
    path('index/register/', index.index_register),
    path('index/login/', index.index_login),
    path('index/logout/', index.logout),
    path('api/', index.AppletApi.isRequestUrl),
    # 登录
    path('bbs/login/', account.login),
    #注销
    path('bbs/logout/', account.logout),
    # 验证码
    path('image/code/', account.image_code),

    # 管理员管理
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/<int:nid>/delete/', views.admin_delete),
    path('admin/<int:nid>/reset/', views.admin_reset),




    re_path(r"^static/(?P<path>.*)$", static_serve,
            {"document_root": settings.STATIC_ROOT}, name='static'),
]
