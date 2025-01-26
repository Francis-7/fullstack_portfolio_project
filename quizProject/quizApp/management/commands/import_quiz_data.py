import csv
from django.core.management.base import BaseCommand
from quizApp.models import Quiz, Question, Choice

class Command(BaseCommand):
    help = "Imports quiz data from CSV files into the database"

    def handle(self, *args, **kwargs):
        # Import quizzes from quizzes.csv
        with open('path_to_your_csv/quizzes.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                quiz = Quiz.objects.create(
                    name=row['quiz_name'],
                    description=row['description'],
                    time=int(row['time_duration (sec)'])
                )
                self.stdout.write(self.style.SUCCESS(f"Quiz '{quiz.name}' imported successfully"))

        # Import questions from questions.csv
        with open('path_to_your_csv/questions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                quiz = Quiz.objects.get(id=row['quiz_id'])
                question = Question.objects.create(
                    quiz=quiz,
                    question_num=row['question_num'],
                    question=row['question'],
                    author=row['author']
                )
                self.stdout.write(self.style.SUCCESS(f"Question '{question.question}' imported successfully"))

        # Import choices from choices.csv
        with open('path_to_your_csv/choices.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question = Question.objects.get(id=row['question_id'])
                choice = Choice.objects.create(
                    question=question,
                    choice=row['choice'],
                    answer_to_question=row['answer_to_question'],
                    is_correct=row['is_correct'] == 'True'
                )
                self.stdout.write(self.style.SUCCESS(f"Choice '{choice.choice}' imported successfully"))
