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