from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField


User = get_user_model()

class RegisterForm(forms.Form):
    """
    注册表单
    """
    name = forms.CharField(label='姓名', required=True)
    username = forms.CharField(label='用户名', required=True)
    college = forms.CharField(label='学院', required=True)
    major = forms.CharField(label='专业', required=True)
    birthday = forms.DateTimeField(label='生日', required=True)
    email = forms.EmailField(label='邮箱', required=True)
    qq_num = forms.CharField(label='QQ号', required=True)
    password = forms.CharField(label='密码', required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError('用户已存在!')
        return username


class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(label='用户名', required=True)
    password = forms.CharField(label='密码', required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if not user:
            raise ValidationError('用户不存在!')
        return username


class ResetPWForm(forms.Form):
    """
    重新设置密码表单
    """
    password1 = forms.CharField(label='原密码', required=True)
    password2 = forms.CharField(label='新密码', required=True)


class TagForm(forms.Form):
    """
    添加标签表单
    """
    master_type_name = forms.CharField(label='标签', required=True)


#用于验证邮箱格式和验证码
class ForgetForm(forms.Form):
    email = forms.CharField(required=True)  # 用户名不能为空
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})

#reset.html中，用于验证新设的密码长度是否达标
class ResetForm(forms.Form):
    newpwd1 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空', 'min_length' : '至少为6位'})
    newpwd2 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})

# 用户修改密码时的表单，注意字段与前端页面保持一致
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)  # 新密码不能为空
    password2 = forms.CharField(required=True, min_length=5)  # 确认密码不能为空