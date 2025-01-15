from rest_framework import serializers
from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Choice
    fields = ['id', 'choice', 'answer_to_question', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
  