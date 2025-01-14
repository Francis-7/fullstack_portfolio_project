from django.db import models

class Question(models.Model):
  question_num = models.IntegerField(primary_key=True)
  question = models.TextField(unique=True)
  author = models.CharField(max_length=30)

  class Meta:
    db_table = 'questions'
    ordering = ['question_num']

    def __str__(self):
      return f"Question {self.question_num} by {self.author}"
    
class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="all_questions")
  Options = models.TextChoices('Options', 'A B C D')
  choice = models.CharField(max_length=1, choices=Options, unique=True)
  answer_to_question = models.TextField(unique=True)
