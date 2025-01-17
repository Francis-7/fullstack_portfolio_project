from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Question, Choice, Score, UserAnswer, QuizSession, Quiz
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import QuestionSerializer, QuizSerializer
from django.utils import timezone

# Registration view
def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      auth_login(request, user)
      messages.success(request, 'Registration Successful!')
      return redirect('login')
    else:
      messages.error(request, 'Error in Registration')
  else:
    form = UserRegistrationForm()
  return render(request, 'quizApp/register.html', {'form' : form})

# login the user view
def login_view(request):
  if request.method == 'POST':
    form = UserLoginForm(data=request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        auth_login(request, user)
        messages.success(request, 'Login Successful')
        next_url = request.GET.get('next', 'dashboard')
        return redirect(next_url)
      else:
        messages.error(request, 'Invalid username or password')
  else:
    form = UserLoginForm()
  return render(request, 'quizApp/login.html', {'form' : form})

# logout a user
def logout_view(request):
  auth_logout(request)
  messages.success(request, 'You have successfully logged out!')
  return redirect('login')

# home view
def home(request):
  return render(request, 'quizApp/home.html')

# user dashboard view
@login_required
def dashboard(request):
  # profile, created = UserProfile.objects.get_or_create(user=request.user)

  try:
      profile = UserProfile.objects.get(user=request.user)
  except UserProfile.DoesNotExist:
      profile = None  # Handle the case where no profile exists for the user

  return render(request, 'quizApp/dashboard.html', {'profile': profile})
  

class QuestionList(generics.ListAPIView):
  queryset = Question.objects.all()
  serializer_class = QuestionSerializer
  permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class QuestionListView(APIView):
  def get(self, request, format=None):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
def quiz_page(request, quiz_id):
  quiz = Quiz.objects.get(id=quiz_id)
  questions = quiz.questions.all()
  return render(request, 'quiz/quiz_page.html', {'quiz_name': quiz.name, 'questions': questions})
 
@login_required
def calculate_score(request):
  user = request.user
  session = QuizSession.objects.get_or_create(user=user)[0]
  if session.is_time_up():
    return JsonResponse({'error': 'Time is up! You cannot submit the quiz now.'})

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
    
    score = (correct_answers / total_questions) * 100
    Score.objects.create(user=user, score=score, date_recorded=timezone.now(), quiz_name="")
    return JsonResponse({'score': score, 'correct_answers': correct_answers, 'total_questions': total_questions})
  
  return redirect('quiz_page')

class QuizListView(APIView):
  def get(self, request, format=None):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class QuizList(generics.ListAPIView):
  queryset = Quiz.objects.all()
  serializer_class = QuizSerializer
  permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()