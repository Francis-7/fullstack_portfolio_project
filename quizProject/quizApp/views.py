from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Registration view
def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, 'Registration Successful!')
      return redirect('login')
    else:
      messages.error(request, 'Error in Registration')
  else:
    form = UserRegistrationForm()
  return render(request, 'quizApp/register.html', {'form' : form})

# login the user view
def login(request):
  if request.method == 'POST':
    form = UserLoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user)
        messages.success(request, 'Login Successful')
        return redirect('dashboard')
      else:
        messages.error(request, 'Invalid username or password')
    else:
      messages.error(request, 'Invalid form submission')
  else:
    form = UserLoginForm()
  return render(request, 'quizApp/login.html', {'form' : form})



