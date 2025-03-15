from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.


"""
基类：可以把通用的字段定义这里，其他地方继承基类即可拥有
"""
class BaseModel(models.Model):
    delete_choices = ((0, '删除'), (1, '正常'))
    is_delete = models.SmallIntegerField(verbose_name='逻辑删除', choices=delete_choices, default=1)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)

    class Meta:
        abstract = True

class Department(BaseModel):
    """部门表"""
    name = models.CharField(verbose_name='部门名称', max_length=20)


class UserInfo(BaseModel):
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


class Case(BaseModel):
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

class Admin(BaseModel):
    """管理员表"""
    login_name  = models.CharField(verbose_name='用户名', max_length=28)
    name = models.CharField(verbose_name='姓名', max_length=22, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    mobile = models.CharField(verbose_name='手机号', max_length=22, null=True, blank=True)

class UserManager(BaseModel):
    """会员信息"""
    login_name  = models.CharField(verbose_name='账号', max_length=28)
    name = models.CharField(verbose_name='昵称', max_length=22, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    expiry_date = models.DateTimeField(verbose_name="授权到期时间",null=True, blank=True)
    band_shop_max = models.SmallIntegerField(verbose_name='绑定店铺最大数量', default=1)

class ShopManager(BaseModel):
    """店铺管理"""
    shop_name  = models.CharField(verbose_name='店铺用户名', max_length=28)
    type_choices = ((1, '拼多多'), (2, '淘宝'), (3, '抖店'), (4, '京东'))
    type = models.SmallIntegerField(verbose_name='绑定店铺', choices=type_choices)
    user = models.ForeignKey(to='UserManager', to_field='id', on_delete=models.CASCADE)

class MemberModel(BaseModel):
    """会员模板"""
    name = models.CharField(verbose_name='名称', max_length=22, null=True, blank=True)
    quantity = models.SmallIntegerField(verbose_name='数量(单位：月)',null=True, blank=True)
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2, default=0)
    remark  = models.CharField(verbose_name='备注', max_length=28, null=True, blank=True)

class MemberRecord(BaseModel):
    """充值记录"""
    order_no = models.CharField(verbose_name='订单号', max_length=32, null=True, blank=True)
    pay_type_choices = ((1, '支付宝'), (2, '微信'))
    pay_type = models.SmallIntegerField(verbose_name='支付方式', choices=pay_type_choices)
    user = models.ForeignKey(to='UserManager', to_field='id', on_delete=models.CASCADE)
    memer = models.ForeignKey(to='MemberModel', to_field='id', on_delete=models.CASCADE)


class messagesLog(BaseModel):
    """人工消息记录"""
    user = models.ForeignKey(to='UserManager', to_field='id', on_delete=models.CASCADE)
    shop = models.ForeignKey(to='ShopManager', to_field='id', on_delete=models.CASCADE)
    shop_user_id = models.SmallIntegerField(verbose_name='店铺用户ID', null=True, blank=True)
    receive_message = models.TextField(verbose_name='接受消息内容', null=True, blank=True)
    send_message = models.TextField(verbose_name='发送消息内容',  null=True, blank=True)
