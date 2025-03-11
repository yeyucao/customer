from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from bbs import models
from django import forms
from django.core.validators import RegexValidator
from bbs.utils.form import AdminEditModelForm, AdminModelForm
from bbs.utils.pagination import Pagination


# Create your views here.



def depart_list(request):
    """部门列表"""
    # 查询所有部门
    data_dict = {}
    # 获取浏览器传过来的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
    depart_set = models.Department.objects.filter(**data_dict).order_by('-id')
    # 实例化封装的分页
    page_object = Pagination(request, depart_set)
    context = {
        "search_data": search_data,  # 查询
        "depart_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'depart_list.html', context)



def depart_add(request):
    """新增部门"""
    # 新增部门
    # return HttpResponse("成功")
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    depart_name = request.POST.get("departname")
    models.Department.objects.create(name=depart_name)
    return redirect('/depart/list')


def depart_delete(request):
    """删除部门"""
    depart_id = request.GET.get("departid")
    models.Department.objects.filter(id=depart_id).delete()
    return redirect('/depart/list')


def depart_edit(request, nid):
    """编辑部门"""
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id, row_object.name)
        return render(request, 'depart_edit.html', {"row_object": row_object})
    # 获取用户提交的部门名称
    edit_depart_name = request.POST.get("departname")
    # 根据编辑页面用户ID去更新部门的名称
    models.Department.objects.filter(id=nid).update(name=edit_depart_name)
    return redirect('/depart/list')


def user_list(request):
    """用户列表"""
    # 查询所有用户
    # 查询所有用例
    data_dict = {}
    # 获取浏览器传过来的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    user_set = models.UserInfo.objects.filter(**data_dict).order_by('-id')
    # 实例化封装的分页
    page_object = Pagination(request, user_set)
    context = {
        "search_data": search_data,  # 查询
        "user_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'user_list.html', context)



def user_add(request):
    """新增用户（原始方式）"""

    if request.method == 'GET':
        # 这个是为了新增页面动态获取性别
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)
    user_name = request.POST.get("username")
    password = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("ac")
    create_time = request.POST.get("ctime")
    gender = request.POST.get("gd")
    depart_id = request.POST.get("dp")
    models.UserInfo.objects.create(name=user_name, password=password,
                                   age=age, account=account,
                                   create_time=create_time,
                                   gender=gender, depart_id=depart_id)
    return redirect('/user/list')


class UserModelForm(forms.ModelForm):
    # 限制姓名的长度，至少为3位
    name = forms.CharField(min_length=3, label='用户名')

    # password = forms.CharField(label='密码',validators='这里写正则表达式')

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        '''widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "age": forms.TextInput(attrs={"class": "form-control"}),
            "account": forms.TextInput(attrs={"class": "form-control"})           
        }'''  # 下方方法更好

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加了class: "from-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """新增用户（ModelForm方式）"""

    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，这里判断的是所有字段不能为空，则存储到数据库
        # models.UserInfo.objects.create(..) 常规存储方式
        form.save()
        return redirect('/user/list')
    # 如果不满足if判断进入到else返回错误信息
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """编辑用户"""
    # 根据nid去数据库获取所在行数据
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 如果数据合法，这里判断的是所有字段不能为空，则存储到数据库
        # models.UserInfo.objects.create(..) 常规存储方式
        # form.instance.字段名=值  # 如果需要存储用户输入之外的值使用这个
        form.save()
        return redirect('/user/list')
        # 如果不满足if判断进入到else返回错误信息
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    """删除用户"""
    # 根据nid去数据库获取所在行数据进行删除
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')


def case_list(request):
    """用例列表"""
    # 查询所有用例
    data_dict = {}
    # 获取浏览器传过来的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
    case_set = models.Case.objects.filter(**data_dict).order_by('-id')
    # 实例化封装的分页
    page_object = Pagination(request, case_set)
    context = {
        "search_data": search_data,  # 查询
        "case_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'case_list.html', context)


class CaseModelForm(forms.ModelForm):
    number = forms.CharField(
        label="用例编号",
        validators=[RegexValidator(r'^0\d{3}$', '数字必须以0开头的4位数字')],
    )

    class Meta:
        model = models.Case
        # fields = ["number", "name", "step", "expect", "actual", "priority", "author", "status", "bug_no"]
        fields = "__all__"  # 这个表示所有字段
        # exclude = ["bug_no"] #  排除字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加了class: "from-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 钩子函数进行判重验证,这个名字注意是clean_加字段名
    def clean_number(self):
        tex_number = self.cleaned_data['number']
        exists = models.Case.objects.filter(number=tex_number).exists()
        if exists:
            raise ValidationError("用例编号已存在")
        return tex_number


def case_add(request):
    """新增用例（ModelForm方式）"""
    if request.method == 'GET':
        form = CaseModelForm()
        return render(request, 'case_add.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = CaseModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，这里判断的是所有字段不能为空，则存储到数据库
        # models.UserInfo.objects.create(..) 常规存储方式
        form.save()
        return redirect('/case/list')
    # 如果不满足if判断进入到else返回错误信息
    return render(request, 'case_add.html', {"form": form})


class CaseEditModelForm(forms.ModelForm):
    # 控制字段显示，但是不可编辑
    number = forms.CharField(disabled=True, label="用例编号")

    class Meta:
        model = models.Case
        fields = ["number", "name", "step", "expect", "actual", "priority", "author", "status", "bug_no"]

        # fields = "__all__"  # 这个表示所有字段
        # exclude = ["bug_no"] #  排除字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加了class: "from-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 钩子函数进行判重验证,这个名字注意是clean_加字段名
    def clean_number(self):
        # 获取当前编辑那一行的ID,从POST那里获取到了instance
        # print(self.instance.pk)
        tex_number = self.cleaned_data['number']
        exists = models.Case.objects.exclude(id=self.instance.pk).filter(number=tex_number).exists()
        if exists:
            raise ValidationError("用例编号已存在")
        return tex_number


def case_edit(request, nid):
    """编辑用户"""
    # 根据nid去数据库获取所在行数据
    row_object = models.Case.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = CaseEditModelForm(instance=row_object)
        return render(request, 'case_edit.html', {"form": form})
    # POST 请求提交的数据，数据校验
    form = CaseEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 如果数据合法，这里判断的是所有字段不能为空，则存储到数据库
        # models.UserInfo.objects.create(..) 常规存储方式
        # form.instance.字段名=值  # 如果需要存储用户输入之外的值使用这个
        form.save()
        return redirect('/case/list')
        # 如果不满足if判断进入到else返回错误信息
    return render(request, 'case_edit.html', {"form": form})


def case_delete(request, nid):
    """删除用例"""
    # 根据nid去数据库获取所在行数据进行删除
    models.Case.objects.filter(id=nid).delete()
    return redirect('/case/list')


def admin_list(request):
    """管理员列表"""
    # 查询所有用例
    data_dict = {}
    # 获取浏览器传过来的值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["login_name__contains"] = search_data
    depart_set = models.Admin.objects.filter(**data_dict)
    # 实例化分页方法
    page_object = Pagination(request, depart_set)
    context = {
        "search_data": search_data,  # 查询
        "depart_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    """新增管理员"""
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {"form": form, "title": "新增管理员"})
    # POST 请求提交的数据，数据校验
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，这里判断的是所有字段不能为空，则存储到数据库
        # models.UserInfo.objects.create(..) 常规存储方式
        form.save()
        return redirect('/admin/list')
    # 如果不满足if判断进入到else返回错误信息
    return render(request, 'change.html', {"form": form, "title": "新增管理员"})


def admin_edit(request, nid):
    """编辑管理"""
    # 根据nid去数据库获取所在行数据
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return redirect('/admin/list')
        render(request, 'error.html', {'msg': "数据不存在"})
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": "编辑管理员"})
    # POST 请求提交的数据，数据校验
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
        # 如果不满足if判断进入到else返回错误信息
    return render(request, 'change.html', {"form": form, "title": "编辑管理员"})


def admin_delete(request, nid):
    """删除管理员"""
    # 根据nid去数据库获取所在行数据进行删除
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list')


def admin_reset(request):
    return None

