from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Quiz(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  number_of_questions = models.IntegerField(default=1)
  time = models.IntegerField(help_text="Duration of the quiz in seconds", default="120")
  


  class Meta:
    ordering = ['name']
    db_table = 'quiz_table'
    verbose_name_plural = 'Quizzes'

  def __str__(self):
    return f"{self.name}"
  
  def get_questions(self):
        return self.question_set.all()
  
class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  question_num = models.IntegerField(primary_key=True)
  question = models.TextField(unique=True)
  author = models.CharField(max_length=30)

  class Meta:
    db_table = 'questions'
    ordering = ['question_num']

  def __str__(self):
    return f"{self.question}"
    
class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, default='{question.question}')
  Options = models.TextChoices('Options', 'A B C D')
  choice = models.CharField(max_length=1, choices=Options)
  answer_to_question = models.TextField(default="your answer")
  is_correct = models.BooleanField(default=False)

  class Meta:
    db_table = 'choices'
    ordering = ['id']

  def __str__(self):
    return f"{self.choice}: {self.answer_to_question}"


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
  question = models.ManyToManyField(Question)
  choice = models.ManyToManyField(Choice)
  profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

  

class Score(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=1)
  score = models.IntegerField()
  date_recorded = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'scores'
    ordering = ['-date_recorded']
    unique_together = ('user', 'quiz')
  
  def __str__(self):
    return f"{self.user.username} - {self.score} ({self.date_recorded})"

class UserAnswer(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=1)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
  is_correct = models.BooleanField(default=False)

  class Meta:
    db_table = 'user_answer'
    # unique_together = ('user', 'question')
  
  def __str__(self):
    return f"{self.user.username} answered {self.choice.choice} for {self.question.question}"
  
class QuizSession(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_session', default=1)
  start_time = models.DateTimeField(default=timezone.now)
  end_time = models.DateTimeField(null=True, blank=True)

  def start_quiz(self):
        # Use the quiz duration (in seconds) from the related Quiz object to set the end time
        quiz_duration = self.quiz.time  # quiz.time is in seconds
        self.end_time = self.start_time + timedelta(seconds=quiz_duration)
        self.save()

  def is_time_up(self):
    if self.end_time:
      return timezone.now() > self.end_time
    return False