from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages

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


