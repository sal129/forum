from django import forms
from .models import User, Post, Reply

class RegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password', 'email')

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'content')

class ReplyForm(forms.ModelForm):
	class Meta:
		model = Reply
		fields = ('content')