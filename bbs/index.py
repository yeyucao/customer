import os
import random
from datetime import  timedelta
from urllib import parse

from alipay import AliPay
from django import forms
from django.core.validators import RegexValidator
from django.db.transaction import atomic
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from bbs import models
from bbs.models import UserManager, CurrentVersion
from bbs.payment.utils import my_ali_pay
from bbs.utils.bootstrap import BootStrapForm
from bbs.utils.code import check_code
from bbs.utils.encrypt import md5
from django.shortcuts import render, redirect
from django.forms import widgets, model_to_dict
from django.utils import timezone


from customer import settings


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
        request.session["info"] = {'id': user_manager_object.id, 'name': user_manager_object.login_name}
        request.session.set_expiry(60 * 60 * 24)
        user_manager_object.password = None
        user_manager_object.expiry_date = user_manager_object.expiry_date.strftime("%Y-%m-%d %H:%M:%S")
        memberModel = models.MemberModel.objects.filter(is_delete__exact=1).values('id', 'name', 'price', 'remark')
        return render(request, 'user_info.html', {'user': user_manager_object,'members':memberModel})

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
        user = models.UserManager.objects.create(login_name=login_name, password=password, expiry_date=months_later,band_shop_max=band_shop_max,inviter_code=inviter_code)
        user_id = user.pk
        img, code_string = check_code()
        invite_code = code_string.upper()
        invite_code = str(user_id) + invite_code
        models.UserManager.objects.filter(id=user_id).update(invite_code=invite_code)
        return render(request, 'register_status.html', {})

    return render(request, 'index_register.html', {'form': form})



class AppletApi(View):

    # Json
    def resJson(code, data, safe=False):
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
        url = request.GET.get('api_uri')

        # 用户登录
        if url == 'user_login':
            return AppletApi.userLogin(request)
        # 店铺绑定
        elif url =='shop_bind':
            return AppletApi.shopBind(request)
        # 获取客户端版本
        elif url == 'version_index':
            return AppletApi.getVersionIndex(request)
        # 获取用户信息
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

    def getVersionIndex(self):
        current_versions = models.CurrentVersion.objects.filter(is_delete__exact=1).order_by('-id')[0:10]
        current = []
        for ret in current_versions:
            current.append(model_to_dict(ret))
        return AppletApi.resJson(code=200, data=current)


def logout(request):
    request.session.clear()
    return redirect('/index/login/')


def pay(request):
    print(request.POST)
    member_id_str = request.POST.get('member_id')
    if member_id_str:
        print(member_id_str)
        member_id = int(member_id_str)
        memberModel = models.MemberModel.objects.filter(is_delete__exact=1,id__exact=member_id).first()
        if memberModel:
            info = request.session.get('info')
            order_no = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(map(str, random.sample(range(0, 9), 6)))
            models.MemberRecord.objects.create(user_id=info.get('id'), memer_id=member_id, pay_type=1,order_no=order_no,price=memberModel.price,pay_status=0)
            # 生成支付宝支付链接地址
            notify_url = "http://127.0.0.1:8000/index/pay_result/"
            alipay = AliPay(
                appid=settings.ALI_PAY_APP_ID,
                app_notify_url=None,
                app_private_key_string=settings.ALIPAY_PRIVATE_KEY_STRING,
                alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
                sign_type="RSA2",
            )
            ## 实例化订单
            order_string = alipay.api_alipay_trade_page_pay(
                subject=memberModel.remark,  ## 交易主题
                out_trade_no=order_no,  ## 订单号
                total_amount=str(memberModel.price),  ## 交易总金额
                return_url=notify_url,  ##  请求支付，之后及时回调的一个接口
                notify_url=None  ##  通知地址，
            )
            ##   发送支付请求
            ## 请求地址  支付网关 + 实例化订单
            result = "https://openapi-sandbox.dl.alipaydev.com/gateway.do?" + order_string
            print(result)

            return redirect(result)
        else:
            print(f'memberModel is None')
            return JsonResponse(dict(ali_pay_url=""))

    else:
        print(f'member_id is None')
    pass


@csrf_exempt
def pay_result(request):
    """
    前端同步回调通知（支付完成后，前端url会接收支付宝支付完成后回传的form参数，将其全部传给该接口进行验签），参数示例如下：
    ?charset=utf-8&out_trade_no=20200808154711123456&method=alipay.trade.page.pay.return&total_amount=0.01&sign=FtDkDtsDE9dW3RB18BfiAeFqkSQAK......E1wE9tgsoUi50%2B0IH7w%3D%3D&trade_no=2020080622001460481436975535&auth_app_id=2016101000655892&version=1.0&app_id=2016101000655892&sign_type=RSA2&seller_id=2087811328364696&timestamp=2020-08-06+12%3A44%3A44
    :return: 根据业务需求自定义返回信息
    """
    if request.method == "GET":
        data = request.GET.dict()

        ali_pay = my_ali_pay()
        sign = data.pop('sign', None)
        success = ali_pay.verify(data, sign)
        print("同步回调验签状态: ", data)
        if success:
            # 修改订单状态
            models.MemberRecord.objects.filter(order_no=data.get('out_trade_no')).update(pay_status=1,last_modify_time=timezone.now())
            record = models.MemberRecord.objects.filter(order_no__exact=data.get('out_trade_no')).first()
            model =models.MemberModel.objects.filter(id__exact=record.memer_id).first()
            user = models.UserManager.objects.filter(id__exact=record.user_id).first()
            months_later = user.expiry_date + timedelta(days=model.quantity * 30)
            models.UserManager.objects.filter(id__exact=record.user_id).update(expiry_date=months_later,last_modify_time=timezone.now())
            return render(request, 'payresult.html',{'remark':model.remark,
                                                     'trade_no':data.get('out_trade_no'),
                                                     'price':record.price,
                                                      'last_modify_time':record.last_modify_time.strftime('%Y-%m-%d %H:%M:%S')})

        return JsonResponse(dict(message="支付失败"))

    return JsonResponse(dict(message="支付失败"))

