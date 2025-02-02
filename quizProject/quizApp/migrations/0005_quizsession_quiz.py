# Generated by Django 5.1.5 on 2025-01-19 04:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizApp", "0004_alter_userprofile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizsession",
            name="quiz",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="quiz_session",
                to="quizApp.quiz",
            ),
        ),
    ]
