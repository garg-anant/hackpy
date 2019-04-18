from django import forms

from .models import Comments, ProfileUser, NewsLinks

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ['content']

class RegisterUser(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = ProfileUser
		fields = ('username', 'password')

class AddLink(forms.ModelForm):

	class Meta:
		model = NewsLinks
		fields = ('title','title_link')