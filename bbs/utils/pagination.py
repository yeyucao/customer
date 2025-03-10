# -*- coding: utf-8 -*-
# @Time    : 2023/2/20 15:24
# @Author  : caicloud
# @File    : pagination.py
# @Software: PyCharm
# @Describe: 自定义分页组件
"""
这个翻页组件的使用说明（视图函数中）：
def case_list(request):
    # 第一步查询数据
    case_set = models.Case.objects.all()
    # 第二步实例化封装的分页对象
    page_object = Pagination(request, case_set)
    context = {
        "case_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'case_list.html', context)
html页面：
        <ul class="pagination">
            {{ page_string }}
        </ul>
"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param='page', plus=5):
        """
        :param request: 请求对象
        :param queryset: 查询符合条件的数据，根据这个数据进行分页处理
        :param page_size: 每页显示多少条数据
        :param page_param:在url中传递的获取分页的参数，例如/case/list/?page=5
        :param plus:显示当前页的前plus页 或后 plus页
        """
        # 以下是为了解决查询翻页查询条件保留的问题
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        # ########################################
        self.page_param = page_param
        page = request.GET.get(self.page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * self.page_size
        self.page_queryset = queryset[self.start: self.end]
        # 数据总条数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        self.plus = plus

    def html(self):
        # 计算出，线上当前页的前5页，后5页，plus=5
        # 数据未到达11页（数据量不达标时）
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 当前页< 5（前面的异常考虑）
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页+plus大于总页面（后面的异常考虑）
                if self.page + self.plus > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    # 前五页，后五页
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        # 首页
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)

            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        # 跳转
        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page"
                           style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0"
                           type="text"  class="form-control" placeholder="页码">
                        <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                    </span>
                </form>
            </li>
            """
        page_str_list.append(search_string)
        # 拼接html
        page_string = mark_safe("".join(page_str_list))
        return page_string