from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
  first_name = forms.CharField(max_length=40)
  last_name = forms.CharField(max_length=40)
  email = forms.EmailField(required=True)

  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

  # def save(self, commit=True):
  #   user = super().save(commit=False)
  #   if commit:
  #     user.save()
  #     UserProfile.objects.create(user=user)
  #   return user
  

class UserLoginForm(AuthenticationForm):
  username = forms.CharField(max_length=50)
  password = forms.CharField(widget=forms.PasswordInput)