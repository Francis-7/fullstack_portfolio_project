# Generated by Django 5.1.5 on 2025-01-24 11:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizApp", "0007_alter_choice_answer_to_question"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="score",
            name="quiz_name",
        ),
        migrations.AddField(
            model_name="score",
            name="quiz",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="quizApp.quiz",
            ),
        ),
    ]
