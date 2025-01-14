from django.contrib import admin
from .models import Question, Choice
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display = ['question_num', 'question', 'author']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
  list_display = ['choice', 'answer_to_question', 'question_tag']

  def question_tag(self, obj):
    question = obj.question
    if not question:
      return format_html("<i>None</i>")
    
    return format_html('<a href="{}">{}</a>', reverse("admin:quizApp_question_change", args=[question.question_num]), question)
  question_tag.short_description = "Questions"
