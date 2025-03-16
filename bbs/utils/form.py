from django import forms
from bbs.utils.bootstrap import BootStrapModelForm, BootStrapForm
from bbs.utils.encrypt import md5
from bbs import models
from django.core.exceptions import ValidationError


class AdminModelForm(BootStrapModelForm):
    login_name = forms.CharField(min_length=6, label='登录账户')
    name = forms.CharField(min_length=2, label='姓名')
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))
    mobile = forms.CharField(label='手机号')

    class Meta:
        model = models.Admin
        fields = ["login_name", "name", "password", "confirm_password","mobile"]
        widgets = {"password": forms.PasswordInput(render_value=True)}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        print(pwd)
        return md5(pwd)

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.Admin.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        # print(pwd)
        confirm = md5(self.cleaned_data.get("confirm_password"))
        # print("第二次密码", confirm)
        if pwd != confirm:
            raise ValidationError("两次密码输入不一致，请重新输入")
        # return 什么以后就保存到数据库是什么
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    login_name = forms.CharField(disabled=True, label='登录账户')

    class Meta:
        model = models.Admin
        fields = ["login_name", "name"]


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {"password": forms.PasswordInput(render_value=True)}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # 判断重置密码与之前的是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("新密码不能与之前的一致！")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        # print(pwd)
        confirm = md5(self.cleaned_data.get("confirm_password"))
        # print("第二次密码", confirm)
        if pwd != confirm:
            raise ValidationError("两次密码输入不一致，请重新输入")
        # return 什么以后就保存到数据库是什么
        return confirm

