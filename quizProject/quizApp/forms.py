from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    labels = {
      'username' : 'Username',
      'first_name' : 'First Name',
      'last_name' : 'Last Name',
      'email' : 'Email',
      'password1' : 'Password',
      'password2' : 'Confirm Password',
      
    }
    widgets = {
      'username' : forms.TextInput(attrs={'placeholder' : 'e.g john', 'class' : 'form-control'}),
      'first_name' : forms.TextInput(attrs={'placeholder' : 'e.g John', 'class' : 'form-control'}),
      'last_name' : forms.TextInput(attrs={'placeholder' : 'e.g Johny', 'class' : 'form-control'}),
      'email' : forms.EmailInput(attrs={'placeholder' : 'e.g john@gmail.com', 'class' : 'form-control'}),
      'password' : forms.PasswordInput(attrs={'placeholder' : '', 'class' : 'form-control'}),
      'password2' : forms.PasswordInput(attrs={'placeholder' : '', 'class' : 'form-control'}),
      
    }
  

class UserLoginForm(AuthenticationForm):
  username = forms.CharField(max_length=50)
  password = forms.CharField(widget=forms.PasswordInput)

class ProfilePictureForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ['profile_picture']