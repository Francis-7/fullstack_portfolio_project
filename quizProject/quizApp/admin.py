from django.contrib import admin
from .models import Question, Choice

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display = ['question_num', 'question', 'author']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
  list_display = ['question', 'choice', 'answer_to_question']