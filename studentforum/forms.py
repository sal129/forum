from django import forms
from django.contrib.auth.models import User
from .models import Post, Reply, MyUser
from django.utils.translation import ugettext_lazy as _
from django.forms import Widget

class LoginForm(forms.ModelForm):
    username = forms.CharField( label=_("昵称*"),label_suffix='')
    password = forms.CharField( label=_("密码*"),widget=forms.PasswordInput,label_suffix='')
    class Meta:
        model = User
        fields = ('username','password')
		
class RegisterForm(forms.ModelForm):
    username = forms.CharField( label=_("昵称*"),label_suffix='',error_messages={'required': '请输入您的昵称'})
    email = forms.CharField( label=_("邮箱（可选）"),label_suffix='',required=False, error_messages={'required': '请输入您的昵称','invalide':'输入的邮箱格式不正确,请重新输入'})
    password = forms.CharField( label=_("密码*"),widget=forms.PasswordInput,label_suffix='')
    password2 = forms.CharField( label=_("重复确认密码*"),widget=forms.PasswordInput,label_suffix='')
    portrait = forms.ImageField( label=_("头像（可选）"),widget=forms.ClearableFileInput,label_suffix='',required=False)
    portrait.widget.initial_text = _('当前')
    portrait.widget.input_text = _('修改')
    portrait.widget.clear_checkbox_label = _('删除')
    portrait.widget.template_with_initial = (
        '<br />%(initial_text)s<img src="%(initial_url)s" width = "100" height = "100"> '
        '%(clear_template)s<br />%(input_text)s %(input)s'
    )
    intro = forms.CharField( label=_("自我介绍（可选）"), widget=forms.Textarea, label_suffix='',required=False)
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            msg = "两次输入的密码不一致"
            self.add_error('password2', msg)
    class Meta:
        model = User
        fields = ('username','email','password', 'password2','portrait','intro')

class changeForm(forms.ModelForm):
	portrait = forms.ImageField( label=_("头像"),widget=forms.ClearableFileInput,)
	portrait.widget.initial_text = _('当前')
	portrait.widget.input_text = _('修改')
	portrait.widget.clear_checkbox_label = _('清除')
	portrait.widget.template_with_initial = (
        '<br />%(initial_text)s<img src="%(initial_url)s" width = "100" height = "100"> '
        '%(clear_template)s<br />%(input_text)s %(input)s'
    )
	class Meta:
		model = MyUser
		fields = ('intro','portrait')	
class userForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','email')		
		
class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'content')


class ReplyForm(forms.ModelForm):
	class Meta:
		model = Reply
		fields = ('content',)

class PasswordForm(forms.Form):
    password = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput,
    )