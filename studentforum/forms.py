from django import forms
from django.contrib.auth.models import User
from .models import Post, Reply, MyUser
from django.utils.translation import ugettext_lazy as _

class RegisterForm1(forms.ModelForm):
    password = forms.CharField( label=_("password"),widget=forms.PasswordInput,)
    class Meta:
        model = User
        fields = ('username','password')
		
class RegisterForm(forms.ModelForm):
    password = forms.CharField( label=_("password"),widget=forms.PasswordInput,)
    class Meta:
        model = User
        fields = ('username','password')

class changeForm(forms.ModelForm):
	class Meta:
		model = MyUser
		fields = ('intro',)	
class userForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','email',)		
		
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
