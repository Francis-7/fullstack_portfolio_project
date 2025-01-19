from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Quiz(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  


  class Meta:
    ordering = ['name']
    db_table = 'quiz_table'
    verbose_name_plural = 'Quizzes'

  def __str__(self):
    return f"{self.name}"
  
class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
  question_num = models.IntegerField(primary_key=True)
  question = models.TextField(unique=True)
  author = models.CharField(max_length=30)

  class Meta:
    db_table = 'questions'
    ordering = ['question_num']

  def __str__(self):
    return f"{self.question}"
    
class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="all_questions", default='{question.question}')
  Options = models.TextChoices('Options', 'A B C D')
  choice = models.CharField(max_length=1, choices=Options)
  answer_to_question = models.TextField(unique=True, default="your answer")
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

  

class Score(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  score = models.IntegerField()
  date_recorded = models.DateTimeField(auto_now_add=True)
  quiz_name = models.CharField(max_length=30, blank=True, null=True)

  class Meta:
    db_table = 'scores'
    ordering = ['-date_recorded']
  
  def __str__(self):
    return f"{self.user.username} - {self.score} ({self.date_recorded})"

class UserAnswer(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

  class Meta:
    db_table = 'user_answer'
    unique_together = ('user', 'question')
  
  def __str__(self):
    return f"{self.user.username} answered {self.choice.choice} for {self.question.question}"
  
class QuizSession(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_session')
  start_time = models.DateTimeField(auto_now_add=True)
  end_time = models.DateTimeField()

  def start_quiz(self):
    self.end_time = self.start_time + timedelta(minutes=15)

  def is_time_up(self):
    return timezone.now() > self.endtime