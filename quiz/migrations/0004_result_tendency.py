# Generated by Django 5.0.6 on 2024-07-23 05:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0003_question_is_multiple_choice"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="tendency",
            field=models.TextField(blank=True),
        ),
    ]
