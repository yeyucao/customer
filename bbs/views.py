from django.shortcuts import render, redirect, HttpResponse
from bbs import models
from django import forms


def depart_list(request):
    """部门列表"""
    # 查询所有部门
    depart_set = models.Department.objects.all()
    print(depart_set)
    return render(request, 'depart_list.html', {"depart_set": depart_set})

def depart_add(request):
    """新增部门"""
    # 新增部门
    # return HttpResponse("成功")
    if request.method =='GET':
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
    user_set = models.UserInfo.objects.all()
    """
    for obj in user_set:
        print(obj.id, obj.name, obj.password, obj.account, obj.create_time.strftime("%Y-%m-%d-%H-%M-%S"),
              obj.get_gender_display(), obj.depart.name)
    """
    return render(request, 'user_list.html', {"user_set": user_set})


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
        return  render(request, 'user_edit.html', {"form": form})
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