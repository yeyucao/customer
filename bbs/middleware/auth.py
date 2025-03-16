from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):


    def process_request(self, request):
        # 1、排除不需要鉴权的页面
        # request.path_info获取当前访问文件URL
        if request.path_info in ['/bbs/login/','/image/code/','/api/','/index/login/']:
            return
            # 2、读取当前用户的session信息，如果能读到，说明能访问
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 3、没有登录过，返回登录界面
        return redirect('/index/login/')