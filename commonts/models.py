from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.
class UserManager(models.Model):
    """会员信息"""
    login_name  = models.CharField(verbose_name='账号', max_length=28)
    name = models.CharField(verbose_name='昵称', max_length=22, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    expiry_date = models.DateField(verbose_name="授权到期时间",null=True, blank=True)
    delete_choices = ((0, '删除'), (1, '正常'))
    is_delete = models.SmallIntegerField(verbose_name='逻辑删除', choices=delete_choices, default=1)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)

class ShopManager(models.Model):
    """店铺管理"""
    shop_name  = models.CharField(verbose_name='店铺用户名', max_length=28)
    type_choices = ((1, '拼多多'), (2, '淘宝'), (3, '抖店'), (4, '京东'))
    type = models.SmallIntegerField(verbose_name='绑定店铺', choices=type_choices)
    user = models.ForeignKey(to='UserManager', to_field='id', on_delete=models.CASCADE)
    delete_choices = ((0, '删除'), (1, '正常'))
    is_delete = models.SmallIntegerField(verbose_name='逻辑删除', choices=delete_choices, default=1)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)

class MemberModel(models.Model):
    """会员模板"""
    name = models.CharField(verbose_name='名称', max_length=22, null=True, blank=True)
    quantity = models.SmallIntegerField(verbose_name='数量(单位：月)',null=True, blank=True)
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2, default=0)
    remark  = models.CharField(verbose_name='备注', max_length=28, null=True, blank=True)
    delete_choices = ((0, '删除'), (1, '正常'))
    is_delete = models.SmallIntegerField(verbose_name='逻辑删除', choices=delete_choices, default=1)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)

class MemberRecord(models.Model):
    """充值记录"""
    order_no = models.CharField(verbose_name='订单号', max_length=32, null=True, blank=True)
    pay_type_choices = ((1, '支付宝'), (2, '微信'))
    pay_type = models.SmallIntegerField(verbose_name='支付方式', choices=pay_type_choices)
    user = models.ForeignKey(to='UserManager', to_field='id', on_delete=models.CASCADE)
    memer = models.ForeignKey(to='MemberModel', to_field='id', on_delete=models.CASCADE)
    delete_choices = ((0, '删除'), (1, '正常'))
    is_delete = models.SmallIntegerField(verbose_name='逻辑删除', choices=delete_choices, default=1)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)

class messagesLog(models.Model):
    """人工消息记录"""
    user = models.ForeignKey(to='UserManager', to_field='id', on_delete=models.CASCADE)
    shop = models.ForeignKey(to='ShopManager', to_field='id', on_delete=models.CASCADE)
    shop_user_id = models.SmallIntegerField(verbose_name='店铺用户ID', null=True, blank=True)
    receive_message = models.TextField(verbose_name='接受消息内容', null=True, blank=True)
    send_message = models.TextField(verbose_name='发送消息内容',  null=True, blank=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)