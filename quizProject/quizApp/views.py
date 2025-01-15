from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Question, Choice, Score, UserAnswer
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer
from django.utils import timezone

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


# logout a user
def logout(request):
  logout(request)
  return redirect('login')

# home view
def home(request):
  return render(request, 'quizApp/home.html')

# user dashboard view
@login_required
def dashboard(request):
  user_profile = UserProfile.objects.get(user=request.user)
  questions = user_profile.question.all()
  choices = user_profile.choice.all()
  return render(request, 'quizApp/dashboard.html', {'questions' : questions, 'choices' : choices})

class QuestionListView(APIView):
  def get(self, request, format=None):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
@login_required
def calculate_score(request):
  if request.method == 'POST':
    user = request.user
    total_questions = len(request.POST.getlist('question_ids'))
    correct_answers = 0

    for question_id in request.POST.getlist('question_ids'):
      selected_choice = request.POST.get(f"question_{question_id}")

      if selected_choice:
        choice = Choice.objects.get(id=selected_choice)
        user_answer = UserAnswer.objects.create(user=user, question_id=question_id, choice=choice)

        if choice.is_correct():
          correct_answers += 1
    
    score = Score.objects.create(user=user, score=score, date_recorded=timezone.now(), quiz_name=""))
