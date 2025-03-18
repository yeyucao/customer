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
from django.views.static import serve as static_serve
from django.conf.urls.static import static
from bbs import views, account, index
from django.urls import path, include, re_path

urlpatterns = [
    #    path("admin/", admin.site.urls),

    path('index/register/', index.index_register),
    path('index/login/', index.index_login),
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
    # 用例管理
    path('case/list/', views.case_list),
    path('case/add/', views.case_add),
    path('case/<int:nid>/edit/', views.case_edit),
    path('case/<int:nid>/delete/', views.case_delete),

    # 项目管理
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),

    # 用户管理
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/model/form/add/', views.user_model_form_add),  # 新方法实现
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),  # 与部门删除方式不一样

    re_path(r"^static/(?P<path>.*)$", static_serve,
            {"document_root": settings.STATIC_ROOT}, name='static'),
]
