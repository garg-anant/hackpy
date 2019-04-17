from django import forms

from .models import Comments, ProfileUser

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ['content']

class RegisterUser(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = ProfileUser
		fields = ('username', 'password')		