from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, aauthenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Question, Choice, Score, UserAnswer, QuizSession, Quiz
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


from .serializers import QuestionSerializer, QuizSerializer, CreateChoiceSerializer, CreateQuestionSerializer
from django.utils import timezone

# Registration view
def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
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


@login_required
def quiz_page(request, quiz_id):
  quiz = get_object_or_404(Quiz, id=quiz_id)
  questions = quiz.questions.all()
  return render(request, 'quizApp/quiz_page.html', {'quiz': quiz, 'questions': questions})
 
@login_required
def quiz_list(request):
  quizzes = Quiz.objects.all()
  return render(request, 'quizApp/quiz_list.html', {'quizzes' : quizzes})


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



@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
  # create user profile object if user object is new and not loaded from fixture
  if kwargs['created'] and not kwargs['raw']:
    user = kwargs['instance']

    try:
      # double check user profile doesn't exist already
      UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
      # no user profile exists for this user, create one
      UserProfile.objects.create(user=user)

@api_view(['GET', 'POST'])
def quiz_list_view(request, format=None):
  if request.method == 'GET':
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response({'quizzes' : serializer.data})
  if request.method == 'POST':
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def quiz_detail_view(request, id, format=None):
    try:
        quiz = Quiz.objects.get(id=id)
    except Quiz.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Handling GET request
    if request.method == 'GET':
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    # Handling PUT request
    elif request.method == 'PUT':
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handling DELETE request
    elif request.method == 'DELETE':
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)