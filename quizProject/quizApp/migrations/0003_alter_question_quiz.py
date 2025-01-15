# Generated by Django 5.1.4 on 2025-01-15 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizApp", "0002_question_quiz"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="quizApp.quiz",
            ),
        ),
    ]
