# Generated by Django 5.1.5 on 2025-01-22 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizApp", "0006_alter_quizsession_end_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="answer_to_question",
            field=models.TextField(default="your answer"),
        ),
    ]
