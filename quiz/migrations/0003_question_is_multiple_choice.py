# Generated by Django 5.0.6 on 2024-07-23 05:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0002_alter_result_groups"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="is_multiple_choice",
            field=models.BooleanField(default=False),
        ),
    ]
