from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
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

  class Meta:
    db_table = 'choices'
    ordering = ['id']

  def __str__(self):
    return f"{self.choice}: {self.answer_to_question}"


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  question = models.ManyToManyField(Question)
  choice = models.ManyToManyField(Choice)