from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib import messages

# Registration view
def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    
