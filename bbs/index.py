import re
import uuid
from datetime import datetime, timedelta

from django import forms
from django.core.validators import RegexValidator
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from bbs import models
from bbs.models import UserManager
from bbs.utils.bootstrap import BootStrapForm
from bbs.utils.code import check_code
from bbs.utils.encrypt import md5
from django.shortcuts import render, redirect
from django.forms import widgets, model_to_dict
from django.utils import timezone



class IndexLoginRegister(BootStrapForm):
    inviter_code = forms.CharField(
        label="请输入邀请码",
        required=False
    )
    login_name = forms.CharField(
        label="请输入手机号",
        validators=[RegexValidator(r"^(1[34578]\d{9})$", '手机号格式错误'), ],
        required=True
    )
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}),
                                error_messages={"required": "密码不能为空！"})
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'placeholder': '请确认密码'}),
                                error_messages={"required": "重新确认密码！"})
    code = forms.CharField(
        label="请输入验证码",
        widget=forms.TextInput,
        error_messages={"required": "验证码不能为空！"},
        required=True
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("密码必须大于等于6位")
        elif len(password1) > 20:
            raise forms.ValidationError("密码过长")

        return md5(password1)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        pw_md52 = md5(password2)
        if password1 and pw_md52 and password1 != pw_md52:
            raise forms.ValidationError("两次密码不一致，请重新输入")

        return password2



class IndexLogin(BootStrapForm):
    login_name = forms.CharField(
        label="请输入手机号",
        validators=[RegexValidator(r"^(1[34578]\d{9})$", '手机号格式错误!'), ],
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="请输入验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def index_login(request):
    """ 登录 """
    if request.method == "GET":
        form = IndexLogin()
        return render(request, 'index_login.html', {'form': form})
    form = IndexLogin(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'index_login.html', {'form': form})

        user_manager_object  = models.UserManager.objects.filter(login_name__exact=form.cleaned_data['login_name']
                                                                 , password__exact=form.cleaned_data['password']
                                                                 , is_delete__exact=1).first()
        if not user_manager_object:
            form.add_error("username", "用户名或密码错误")
            return render(request, 'index_login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': user_manager_object.id, 'name': user_manager_object.login_name}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24)

        return render(request, 'register_status.html', {})

    return render(request, 'index_login.html', {'form': form})


def index_register(request):
    """ 注册 """
    if request.method == "GET":
        form = IndexLoginRegister()
        return render(request, 'index_register.html', {'form': form})
    form = IndexLoginRegister(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'index_register.html', {'form': form})
        filter_result = UserManager.objects.filter(login_name__exact=form.cleaned_data['login_name'])  # exact精准匹配
        if len(filter_result) > 0:
            form.add_error("login_name", "该手机号已注册！")
            return render(request, 'index_register.html', {'form': form})

        login_name = form.cleaned_data['login_name']
        password = form.cleaned_data['password1']
        inviter_code = form.cleaned_data.get('inviter_code')

        today = timezone.now()
        months_later = today + timedelta(days=1 * 30)
        expiry_date = months_later.strftime("%Y-%m-%d %H:%M:%S")
        band_shop_max = 100
        user = models.UserManager.objects.create(login_name=login_name, password=password, expiry_date=expiry_date,band_shop_max=band_shop_max,inviter_code=inviter_code)
        user_id = user.pk
        img, code_string = check_code()
        invite_code = code_string.upper()
        invite_code = str(user_id) + invite_code
        models.UserManager.objects.filter(id=user_id).update(invite_code=invite_code)
        return render(request, 'register_status.html', {})

    return render(request, 'index_register.html', {'form': form})



class AppletApi(View):

    # Json
    def resJson(code, data, safe=True):
        """
           :param code: 200=>成功;-1->失败
           :param data: 返回的参数
           :return: 输出JSON
           """
        if code == 200:
            json_dict = {'code': 200, 'msg': "成功", 'data': data}
        else:
            json_dict = {'code': -1, 'msg': "失败", 'data': data}
        return JsonResponse(json_dict, safe=safe)

    @csrf_exempt
    def isRequestUrl(request):
        """
        @require_GET
        :return: json
        """
        url = request.POST.get('api_uri')

        # 用户登录
        if url == 'user_login':
            return AppletApi.userLogin(request)
        # 店铺绑定
        elif url =='shop_bind':
            return AppletApi.shopBind(request)
        return AppletApi.resJson(code='-1', data='error')


    def userLogin(request):
        """
        客户端用户登陆
        @require_POST
        :return: json
        """
        login_name = request.POST.get('login_name')
        login_pwd = request.POST.get('login_pwd')
        # 验证用户登录
        if bool(login_name) and bool(login_pwd):
            password = md5(login_pwd)
            res = UserManager.objects.filter(login_name=login_name, password=password).order_by('-id')
            json_dict = {}
            for ret in res:
                json_dict = model_to_dict(ret)
            if json_dict:
                json_dict['password'] = None
                return AppletApi.resJson(code=200, data=json_dict)

        return AppletApi.resJson(code='-1', data='用户名或密码错误')

    def shopBind(request):
        """
        客户端店铺绑定
        @require_POST
        :return: json
        """
        shop_name = request.POST.get('shop_name')
        type = request.POST.get('type')
        is_delete = request.POST.get('is_delete')
        user_id = request.POST.get('user_id')
        models.ShopManager.objects.create(shop_name=shop_name, type=type, is_delete=is_delete, user_id=user_id)
        return AppletApi.resJson(code=200, data='成功')

