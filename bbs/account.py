import json
from io import BytesIO
from turtle import pd

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import HttpResponse
from django.views import View

from bbs import models
from bbs.utils.form import LoginForm
from django.shortcuts import render, redirect



def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(data=request.POST)

    if form.is_valid():
        search_dict = dict()
        search_dict["login_name"] = form.cleaned_data["login_name"]
        search_dict["password"] = form.cleaned_data["password"]
        admin_object = models.Admin.objects.filter(**search_dict).first()
        if not admin_object:
            form.add_error("login_name", "用户名或密码错误！")  # 主动抛出错误显示位置
            return render(request, 'login.html', {"form": form})
        # 用户名密码正确
        # 网站生成随机字符串，写到cookie，再写到session
        request.session['info'] = {
            "id": admin_object.id,
            "login_name": admin_object.login_name,
            "name": admin_object.mobile
        }
        return redirect('/admin/list')
    # 如果不满足if判断进入到else返回错误信息
    return render(request, 'login.html', {"form": form})

# 创建验证码
def captcha():
    hashkey = CaptchaStore.generate_key()   #验证码答案
    image_url = captcha_image_url(hashkey)  #验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha

#刷新验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            if get_captcha.response == captchaStr.lower():     # 如果验证码匹配
                return True
        except:
            return False
    else:
        return False


class IndexView(View):
    def get(self, request):
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return render(request, "login.html", locals())
    def post(self,request):
        capt=request.POST.get("captcha",None)         #用户提交的验证码
        key=request.POST.get("hashkey",None)          #验证码答案
        if jarge_captcha(capt,key):
            return  HttpResponse("验证码正确")
        else:
            return HttpResponse("验证码错误")


def logout(request):
    """注销"""

    return redirect('/login/')

