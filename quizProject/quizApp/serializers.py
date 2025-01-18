from rest_framework import serializers
from .models import Question, Choice, Quiz


class ChoiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Choice
    fields = ['id', 'choice', 'answer_to_question', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
  all_choices = ChoiceSerializer(many=True, read_only=True)

  class Meta:
    model = Question
    fields = ['question_num', 'question', 'author', 'all_choices']


class QuizSerializer(serializers.ModelSerializer):
  questions = QuestionSerializer(many=True, read_only=True)

  class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'questions']