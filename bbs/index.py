from django.forms import model_to_dict
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from bbs import models
from bbs.models import UserManager
from bbs.utils.encrypt import md5


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

