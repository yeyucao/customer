from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from bbs import models
from bbs.utils.encrypt import md5


class UserManagerEditModelForm(forms.ModelForm):
    # 控制字段显示，但是不可编辑
    login_name = forms.CharField(disabled=True, label="会员登陆账号")

    class Meta:
        model = models.UserManager
        fields = ["login_name", "expiry_date"]

        # fields = "__all__"  # 这个表示所有字段
        # exclude = ["bug_no"] #  排除字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加了class: "from-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 钩子函数进行判重验证,这个名字注意是clean_加字段名
    def clean_login_name(self):
        # 获取当前编辑那一行的ID,从POST那里获取到了instance
        # print(self.instance.pk)
        login_name = self.cleaned_data['login_name']
        exists = models.UserManager.objects.exclude(id=self.instance.pk).filter(login_name=login_name).exists()
        if exists:
            raise ValidationError("用户手机号已存在！")
        return login_name

class UserManagerAddModelForm(forms.ModelForm):
    login_name = forms.CharField(
        label="会员登陆账号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    # password = forms.CharField(label='密码',validators='这里写正则表达式')

    class Meta:
        model = models.UserManager
        fields = ["login_name", "name", "password", "mobile", "account", "expiry_date", "invite_code","band_shop_max"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加了class: "from-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_login_name(self):
        login_name = self.cleaned_data['login_name']
        exists = models.UserManager.objects.filter(login_name=login_name).exists()
        if exists:
            raise ValidationError("用户手机号已存在！")
        return login_name
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("密码必须大于等于6位")
        elif len(password) > 20:
            raise forms.ValidationError("密码过长")

        return md5(password)

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        if not invite_code:
            return invite_code
        if len(invite_code) > 6:
            raise forms.ValidationError("邀请码必须小于等于6位")
        elif len(invite_code) < 4:
            raise forms.ValidationError("邀请码必须大于等于4位")

        exists = models.UserManager.objects.filter(invite_code=invite_code).exists()
        if exists:
            raise ValidationError("该邀请码已存在！")
        return invite_code

class MemberModelEditModelForm(forms.ModelForm):

    class Meta:
        model = models.MemberModel
        fields = ["name", "quantity", "price", "remark"]

        # fields = "__all__"  # 这个表示所有字段
        # exclude = ["bug_no"] #  排除字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加了class: "from-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class CurrentVersionAddModelForm(forms.ModelForm):

    # password = forms.CharField(label='密码',validators='这里写正则表达式')

    class Meta:
        model = models.CurrentVersion
        fields = ["old_version", "new_version", "download_url"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加了class: "from-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_old_version(self):
        old_version = self.cleaned_data['old_version']
        exists = models.CurrentVersion.objects.filter(old_version__iexact=old_version,is_delete=1).exists()
        if exists:
            raise ValidationError("原版本号存在记录！")
        return old_version

class CurrentVersionEditModelForm(forms.ModelForm):
    # 控制字段显示，但是不可编辑
    old_version = forms.CharField(disabled=True, label="升级前版本号")
    class Meta:
        model = models.CurrentVersion
        fields = ["old_version", "new_version", "download_url"]

        # fields = "__all__"  # 这个表示所有字段
        # exclude = ["bug_no"] #  排除字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加了class: "from-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
