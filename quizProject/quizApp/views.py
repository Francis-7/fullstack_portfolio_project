from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, aauthenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm, ProfilePictureForm, QuizForm, QuestionForm, ChoiceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
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
  quiz = Quiz.objects.all()
  return render(request, 'quizApp/home.html', {'quiz' : quiz})

# user dashboard view
@login_required
def dashboard(request):
  profile = UserProfile.objects.filter(user=request.user).first()
  scores = Score.objects.filter(user=request.user)
  has_taken_quizzes = scores.exists()

  if request.method == 'POST' and 'update_picture' in request.POST:
     form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
     if form.is_valid():
        form.save()
        return redirect('dashboard')
  else:
      form = ProfilePictureForm(instance=profile)

  return render(request, 'quizApp/dashboard.html', {
        'profile': profile,
        'scores': scores,
        'has_taken_quizzes': has_taken_quizzes,
        'form': form,
        
    })

@login_required
def quiz_page_view(request, id):
  quiz = get_object_or_404(Quiz, id=id)
  questions = quiz.get_questions()
  total_questions = questions.count()
  user_answers = []

  if request.method == 'POST':
     score = 0
     for question in questions:
        selected_choice_id = request.POST.get(f'question_{question.question_num}')
        if selected_choice_id:
           choice = Choice.objects.get(id=selected_choice_id)
           is_correct = choice.is_correct
           UserAnswer.objects.create(user=request.user, quiz=quiz, question=question, choice=choice, is_correct=is_correct)
           if is_correct:
              score += 1
     Score.objects.update_or_create(user=request.user, quiz=quiz, defaults={'score' : score})
     return redirect('submit_quiz', id=id)
  return render(request, 'quizApp/quiz_page.html', {
     'quiz' : quiz,
     'questions' : questions,
     'total_questions' : total_questions
  })
 
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
    
    # Fetch the score
    score = Score.objects.filter(user=request.user, quiz=quiz).first()
    
    if not score:
        # Handle the case where no score exists (this should be rare)
        score = None

    # Get all the questions for the quiz
    questions = quiz.get_questions()

    # Fetch all UserAnswer entries for this user and quiz
    user_answers = UserAnswer.objects.filter(user=request.user, quiz=quiz)

    # Calculate total, attempted, correct, and incorrect answers
    total_questions = questions.count()
    attempted = user_answers.count()
    correct_answers = user_answers.filter(is_correct=True).count()
    incorrect_answers = attempted - correct_answers  # Total attempted minus correct gives incorrect answers

    # Pass the data to the template
    return render(request, 'quizApp/submit_quiz.html', {
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions,
        'attempted': attempted,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'average' : total_questions / 2,
    })


@user_passes_test(lambda u: u.is_superuser)
def add_quiz(request):
   if request.method == 'POST':
      form = QuizForm(data=request.POST)
      if form.is_valid():
         form.save()
         return redirect('dashboard')
   else:
      form = QuizForm()
   return render(request, "quizApp/add_quiz.html", {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def add_question(request):
   if request.method == 'POST':
      form = QuestionForm(data=request.POST)
      if form.is_valid():
         form.save()
         return redirect('dashboard')
   else:
      form = QuestionForm()
   return render(request, "quizApp/add_question.html", {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def add_choice_view(request):
   if request.method == 'POST':
      form = ChoiceForm(data=request.POST)
      if form.is_valid():
         form.save()
         return redirect('dashboard')
   else:
      form = ChoiceForm()
   return render(request, "quizApp/add_choice.html", {'form':form})

from django.shortcuts import render, redirect
from .forms import ChoiceForm
from .models import Quiz, Question

@user_passes_test(lambda u: u.is_superuser)
def add_choice(request):
   if request.method == 'POST':
      form = ChoiceForm(data=request.POST)
      if form.is_valid():
         form.save()
         return redirect('dashboard')  # Redirect to your dashboard or other relevant page
   else:
      # Get the quiz queryset and filter based on the selected quiz
      quiz_list = Quiz.objects.all()

      # Check if a quiz is selected (e.g., through GET or default selection)
      selected_quiz = request.GET.get('quiz')  # Assume the quiz is being passed in the query params

      # If a quiz is selected, filter questions based on the quiz
      if selected_quiz:
         questions = Question.objects.filter(quiz_id=selected_quiz)
      else:
         questions = Question.objects.all()

      form = ChoiceForm()

   return render(request, "quizApp/add_choice.html", {
       'form': form,
       'quiz_list': quiz_list,
       'questions': questions,  # Pass filtered questions to the template
   })




@login_required
def quiz_page_backup(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = quiz.get_questions()
    total_questions = questions.count()

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        # Clear previous answers (to allow the user to retake)
        UserAnswer.objects.filter(user=request.user, quiz=quiz).delete()

        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.question_num}')
            if selected_choice_id:
                choice = Choice.objects.get(id=selected_choice_id)
                is_correct = choice.is_correct
                # Create new UserAnswer for this submission
                UserAnswer.objects.create(
                    user=request.user, quiz=quiz, question=question, choice=choice, is_correct=is_correct)
                
                if is_correct:
                    score += 1
        
        # Update or create the score for the user
        Score.objects.update_or_create(user=request.user, quiz=quiz, defaults={'score': score})

        # Redirect to the submit_quiz page to display the results
        return redirect('submit_quiz', id=id)

    return render(request, 'quizApp/quiz_page.html', {
        'quiz': quiz,
        'questions': questions,
        'total_questions': total_questions
    })


@login_required
def quiz_page(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = quiz.get_questions()
    total_questions = questions.count()

    # Fetch the quiz session or create a new one
    quiz_session, created = QuizSession.objects.get_or_create(user=request.user, quiz=quiz, end_time__isnull=True)
    
    if created:
        # Start the quiz by setting the end time (5 minutes from now)
        quiz_session.start_quiz()

    # Check if the time is up
    if quiz_session.is_time_up():
        return redirect('submit_quiz', id=id)
    
    # Calculate remaining time (in seconds)
    remaining_time = 0
    if quiz_session.end_time:
        remaining_time = (quiz_session.end_time - timezone.now()).total_seconds()

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        # Clear previous answers (to allow the user to retake)
        UserAnswer.objects.filter(user=request.user, quiz=quiz).delete()

        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.question_num}')
            if selected_choice_id:
                choice = Choice.objects.get(id=selected_choice_id)
                is_correct = choice.is_correct
                # Create new UserAnswer for this submission
                UserAnswer.objects.create(
                    user=request.user, quiz=quiz, question=question, choice=choice, is_correct=is_correct)
                
                if is_correct:
                    score += 1
        
        # Update or create the score for the user
        Score.objects.update_or_create(user=request.user, quiz=quiz, defaults={'score': score})

        # Mark the quiz session as ended by setting the end_time
        quiz_session.end_time = timezone.now()
        quiz_session.save()

        # Redirect to the submit_quiz page to display the results
        return redirect('submit_quiz', id=id)
    # remaining_time = quiz_session.remaining_time()
    return render(request, 'quizApp/quiz_page.html', {
        'quiz': quiz,
        'questions': questions,
        'total_questions': total_questions,
        'remaining_time': remaining_time,
    })
