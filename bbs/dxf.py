from django.shortcuts import render, redirect

from bbs import models
from bbs.utils.dxfForm import UserManagerEditModelForm, UserManagerAddModelForm, MemberModelEditModelForm, \
    CurrentVersionAddModelForm, CurrentVersionEditModelForm
from bbs.utils.pagination import Pagination


def user_list(request):
    """会员列表"""
    # 查询所有用例
    data_dict = {}
    # 获取浏览器传过来的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["login_name__contains"] = search_data
    case_set = models.UserManager.objects.filter(**data_dict).order_by('-id')
    # 实例化封装的分页
    page_object = Pagination(request, case_set)
    context = {
        "search_data": search_data,  # 查询
        "case_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'dxf_user_list.html', context)


def user_edit(request, nid):
    # 根据nid去数据库获取所在行数据
    row_object = models.UserManager.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserManagerEditModelForm(instance=row_object)
        return render(request, 'dxf_user_edit.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = UserManagerEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 如果数据合法，这里判断的是所有字段不能为空，则存储到数据库
        # models.UserInfo.objects.create(..) 常规存储方式
        # form.instance.字段名=值  # 如果需要存储用户输入之外的值使用这个
        form.save()
        return redirect('/usermanager/list/')
        # 如果不满足if判断进入到else返回错误信息
    return render(request, 'dxf_user_edit.html', {"form": form})


def user_add(request):
    """新增用户（ModelForm方式）"""

    if request.method == 'GET':
        form = UserManagerAddModelForm()
        return render(request, 'dxf_user_add.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = UserManagerAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/usermanager/list/')
    # 如果不满足if判断进入到else返回错误信息
    return render(request, 'dxf_user_add.html', {"form": form})


def member_model_list(request):
    """充值会员列表"""
    # 查询所有用例
    data_dict = {}
    # 获取浏览器传过来的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
    case_set = models.MemberModel.objects.filter(**data_dict).order_by('-id')
    # 实例化封装的分页
    page_object = Pagination(request, case_set)
    context = {
        "search_data": search_data,  # 查询
        "case_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'dxf_member_model_list.html', context)


def member_model_edit(request, nid):
    # 根据nid去数据库获取所在行数据
    row_object = models.MemberModel.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = MemberModelEditModelForm(instance=row_object)
        return render(request, 'dxf_member_model_edit.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = MemberModelEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 如果数据合法，这里判断的是所有字段不能为空，则存储到数据库
        # models.UserInfo.objects.create(..) 常规存储方式
        # form.instance.字段名=值  # 如果需要存储用户输入之外的值使用这个
        form.save()
        return redirect('/membermodel/list/')
        # 如果不满足if判断进入到else返回错误信息
    return render(request, 'dxf_user_edit.html', {"form": form})


def member_record_list(request):
    # 查询所有用例
    data_dict = {}
    # 获取浏览器传过来的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
    case_set = models.MemberRecord.objects.filter(**data_dict).order_by('-id')
    # 实例化封装的分页
    page_object = Pagination(request, case_set)
    context = {
        "search_data": search_data,  # 查询
        "case_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'dxf_member_record_list.html', context)


def current_version_list(request):
    # 查询所有用例
    data_dict = {}
    # 获取浏览器传过来的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
    case_set = models.CurrentVersion.objects.filter(**data_dict).order_by('-id')
    # 实例化封装的分页
    page_object = Pagination(request, case_set)
    context = {
        "search_data": search_data,  # 查询
        "case_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'dxf_current_version_list.html', context)


def current_version_add(request):
    if request.method == 'GET':
        form = CurrentVersionAddModelForm()
        return render(request, 'dxf_current_version_add.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = CurrentVersionAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/currentversion/list/')
    # 如果不满足if判断进入到else返回错误信息
    return render(request, 'dxf_current_version_add.html', {"form": form})


def current_version_edit(request,nid):
    # 根据nid去数据库获取所在行数据
    row_object = models.CurrentVersion.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = CurrentVersionEditModelForm(instance=row_object)
        return render(request, 'dxf_current_version_edit.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = CurrentVersionEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/currentversion/list/')
        # 如果不满足if判断进入到else返回错误信息
    return render(request, 'dxf_current_version_edit.html', {"form": form})


def current_version_delete(request,nid):
    # 根据nid去数据库获取所在行数据进行删除
    models.CurrentVersion.objects.filter(id=nid).delete()
    return redirect('/currentversion/list/')