from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, aauthenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
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

  try:
      profile = UserProfile.objects.get(user=request.user)

  except UserProfile.DoesNotExist:
      profile = None  # Handle the case where no profile exists for the user
  
  scores = Score.objects.filter(user=request.user)
  # user_answers = UserAnswer.objects.filter(user=request.user)

  return render(request, 'quizApp/dashboard.html', {
        'profile': profile,
        'scores': scores,
        
    })


@login_required
def quiz_page(request, id):
  quiz = get_object_or_404(Quiz, id=id)
  
  if request.method == 'POST':
    
    # Get the score
    score = int(request.POST.get('score', 0))

    # Save the user's submission with score
    Score.objects.create(user=request.user, quiz=quiz, score=score)

    return redirect('submit_quiz', id=id)
  return render(request, 'quizApp/quiz_page.html', {'quiz': quiz})
 
@login_required
def quiz_list(request):
  quizzes = Quiz.objects.all().order_by('created_at')
  return render(request, 'quizApp/quiz_list.html', {'quizzes' : quizzes})



@login_required
def quiz_result(request, id):
  quiz = get_object_or_404(Quiz, id=id)
  user = request.user
  # Get the latest score for the quiz and user
  score = Score.objects.filter(user=user, quiz=quiz).first()
  return render(request, 'quizApp/quiz_result.html', {'quiz' : quiz, 'score' : score})


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
def quiz_questions(request, format=None):
  if request.method == 'GET':
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response({'questions' : serializer.data})
  elif request.method == 'POST':
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
    

from django.http import Http404

@login_required
def submit_quiz_view(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    user = request.user
    # answers = UserAnswer(user=user, question=quiz.questions.all, choice=question.all_questions, quiz=quiz)

    # Check if the user has already completed the quiz session
    # quiz_session = QuizSession.objects.filter(user=user, quiz=quiz, end_time__isnull=True).first()
    # if not quiz_session:
        # raise Http404("Quiz session not found or already completed.")

    score = 0
    total_questions = quiz.questions.count()

    # Loop through each question and get the user's answer
    for question in quiz.questions.all():
        user_choice = request.POST.get(f"question_{question.question_num}")  # Assuming the user selection is in POST data
        if user_choice:
            # Get the corresponding choice for the user’s answer
            choice = Choice.objects.get(id=user_choice)
            # Save the answer
            user_answer, created = UserAnswer.objects.get_or_create(user=user, question=question)
            user_answer.choice = choice
            user_answer.save()

            # Check if the user's answer is correct
            if choice.is_correct:
                score += 1

    # Save the score for the user
    Score.objects.create(user=user, score=score, quiz_name=quiz.name)

    # Mark the quiz session as complete
    # quiz_session.end_time = timezone.now()
    # quiz_session.save()

    # Redirect to a result page or render with the score
    return redirect('quiz_result', id=id)


from django.utils import timezone
from datetime import timedelta

@login_required
def start_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    user = request.user

    # Check if a session already exists, if not create it
    quiz_session, created = QuizSession.objects.get_or_create(user=user, quiz=quiz, end_time__isnull=True)

    if created:
       # If the session is newly created, start it
      quiz_session.start_time = timezone.now()
      quiz_session.end_time = quiz_session.start_time + timedelta(minutes=5)  # Set 5-minute timer
      quiz_session.save()
    return render(request, 'quizApp/start_quiz.html', {'quiz' : quiz})

@login_required
def reset_data(request):
   user = request.user
   scores = Score.objects.filter(user=request.user)
   if request.method == 'POST':
      scores.delete()
      return redirect('dashboard')
   return render(request, 'quizApp/reset_data.html', {'scores' : scores})

@login_required
def submit_quiz(request, id):
   quiz = get_object_or_404(Quiz, id=id)
   score = Score.objects.filter(user=request.user, quiz=quiz).first()

   # If no score is found, you can handle it with a message or set score to 0 (or other logic)
   if not score:
      # Or you could set a default score if needed
      score = None
   return render(request, 'quizApp/submit_quiz.html', {'score' : score})