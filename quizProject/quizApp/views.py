from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib import messages

# Registration view
def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, 'Registration Successful!')
      return redirect('home_page')


