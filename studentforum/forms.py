from django import forms
from django.contrib.auth.models import User
from .models import Post, Reply, MyUser, Letter
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
		fields = ('email',)		
		
class PostForm(forms.ModelForm):
    photo = forms.ImageField( label=_("图片(可选）"),widget=forms.ClearableFileInput,required=False,label_suffix='',error_messages={'invalide':'请输入正确的图片内容'})
    photo.widget.initial_text = _('当前')
    photo.widget.input_text = _('修改')
    photo.widget.clear_checkbox_label = _('清除')
    photo.widget.template_with_initial = (
        '<br />%(initial_text)s<img src="%(initial_url)s" width = "100" height = "100"> '
        '%(clear_template)s<br />%(input_text)s %(input)s'
    )
    attachment = forms.FileField(label=_("附件(可选）"),required=False,label_suffix='',error_messages={'invalide':'请输入正确的文件内容'})
    attachment.widget.initial_text = _('当前')
    attachment.widget.input_text = _('修改')
    attachment.widget.clear_checkbox_label = _('清除')
    title = forms.CharField( label=_("帖子标题"), label_suffix='',error_messages={'required': '请输入帖子的标题'})
    content = forms.CharField( label=_("内容"), widget=forms.Textarea,label_suffix='',error_messages={'required': '请输入帖子的内容'})
    class Meta:
        model = Post
        fields = ('title', 'content','photo','attachment')


class ReplyForm(forms.ModelForm):
    photo = forms.ImageField( label=_("图片（可选）"),widget=forms.ClearableFileInput,required=False,label_suffix='',error_messages={'invalide':'请输入正确的图片内容'})
    photo.widget.initial_text = _('当前')
    photo.widget.input_text = _('修改')
    photo.widget.clear_checkbox_label = _('清除')
    photo.widget.template_with_initial = (
        '<br />%(initial_text)s<img src="%(initial_url)s" width = "100" height = "100"> '
        '%(clear_template)s<br />%(input_text)s %(input)s'
    )
    attachment = forms.FileField(label=_("附件(可选）"),required=False,label_suffix='',error_messages={'invalide':'请输入正确的文件内容'})
    attachment.widget.initial_text = _('当前')
    attachment.widget.input_text = _('修改')
    attachment.widget.clear_checkbox_label = _('清除')
    content = forms.CharField( label=_("回帖内容"), widget=forms.Textarea,label_suffix='',error_messages={'required': '请输入帖子的内容'})
    class Meta:

        model = Reply
        fields = ('content','photo','attachment')

class PasswordForm(forms.Form):
    password = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput,
    )



class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ('content',)

class EditColumnForm(forms.Form):
    value = forms.CharField( label=_("修改为"),label_suffix='',error_messages={'required': '请输入类标的名称','invalid': '请输入正确的类标名称'})

class AddColumnForm(forms.Form):
    value = forms.CharField( label=_("分类名称"),label_suffix=':',error_messages={'required': '请输入待添加的类标名称','invalid': '请输入正确的类标名称'})
		
	

