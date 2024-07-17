# quiz/models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    group = models.CharField(max_length=50)

    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groups = models.TextField()  # Store list of groups as a comma-separated string

    def set_groups(self, groups_list):
        self.groups = ",".join(groups_list)

    def get_groups(self):
        return self.groups.split(",")

    def __str__(self):
        return f'{self.user.username} - {self.groups}'


