from django.db import models


# Create your models here.


class Department(models.Model):
    """部门表"""
    name = models.CharField(verbose_name='部门名称', max_length=20)


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=20)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')
    # depart会自动生成字段为depart_id
    # 级联删除 on_delete=models.CASCADE
    # 置空 on_delete=models.SET_NULL 但是必须和null=True, blank=True配合使用，因为你得支持为null
    depart = models.ForeignKey(to='Department', to_field='id', on_delete=models.CASCADE)


class Case(models.Model):
    """测试用例表"""
    number = models.CharField(verbose_name='用例编号', max_length=11)
    bug_no = models.IntegerField(verbose_name='缺陷编号', null=True, blank=True)
    name = models.CharField(verbose_name='用例名称', max_length=20)
    step = models.CharField(verbose_name='步骤', max_length=150)
    expect = models.CharField(verbose_name='期望结果', max_length=100)
    actual = models.CharField(verbose_name='实际结果', max_length=100)
    author = models.CharField(verbose_name='作者', max_length=20)
    priority_choices = (
        (1, 'P0'),
        (2, 'P1'),
        (3, 'P2'),
        (4, 'P3'),
    )
    priority = models.SmallIntegerField(verbose_name='优先级', choices=priority_choices, default=1)
    status_choices = (
        (1, '未执行'),
        (2, '通过'),
        (3, '未通过'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
