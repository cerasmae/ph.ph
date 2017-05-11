from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


###########################################

from ckeditor.fields import RichTextFormField
# from ckeditor.fields import RichTextUploadingFormField

class CkEditorForm(forms.Form):
	title = forms.CharField(widget=TextInput(attrs={'placeholder': 'Title', 'maxlength': '80'}))
	content = RichTextFormField()
	location = forms.CharField(widget=TextInput(attrs={'placeholder': 'Location', 'maxlength': '30'}))

##########################################

class ImageForm(forms.ModelForm):
	image = forms.ImageField(label='Add a photo')

##########################################

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'password'}))

class SignupForm(UserCreationForm):
	first_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'first name', 'maxlength': '30'}))
	last_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'last name', 'maxlength': '30'}))
	email = forms.CharField(widget=TextInput(attrs={'placeholder': 'email', 'maxlength': '100'}))
	username = forms.CharField(widget=TextInput(attrs={'placeholder': 'username', 'maxlength': '20'}))
	password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'password'}))
	password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'confirm password'}))
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'email',
			'username',
			]

	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_valid = User.objects.filter(email=email)
		print(self.cleaned_data)

		if email_valid.exists():
			raise forms.ValidationError("This email is already registered.")

		return email

	def save(self, commit=True):
		user = super(SignupForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save();
		return user