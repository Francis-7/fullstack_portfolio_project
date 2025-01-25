# Generated by Django 5.1.5 on 2025-01-25 06:38

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizApp", "0010_useranswer_is_correct"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
        ),
        migrations.AlterField(
            model_name="quizsession",
            name="start_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterUniqueTogether(
            name="score",
            unique_together={("user", "quiz")},
        ),
    ]
