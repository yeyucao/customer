from django.http import JsonResponse
from django.views import View


# Create your views here.
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

    # 函数选择器
    def isRequestUrl(request):
        """
        @require_GET
        :return: json
        """
        url = request.GET.get('api_uri')
        # 用户登录
        if url == 'user_login':
            return AppletApi.login(request)
        return AppletApi.resJson(code='-1', data='error')

    def login(self):
        pass


def isRequestUrl(request):
    return None