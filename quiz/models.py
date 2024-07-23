# quiz/models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.TextField()
    is_multiple_choice = models.BooleanField(default=False)  # 新增字段


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
    tendency = models.TextField(blank=True)  # 新增字段

    def set_groups(self, groups_list):
        self.groups = ",".join([group.strip() for group in groups_list])

    def get_groups(self):
        return [group.strip() for group in self.groups.split(",")]

    def update_tendency(self):
        group_list = self.get_groups()
        group_frequency = {}
        for group in group_list:
            if group in group_frequency:
                group_frequency[group] += 1
            else:
                group_frequency[group] = 1
        sorted_groups = sorted(group_frequency.items(), key=lambda x: x[1], reverse=True)
        self.tendency = ",".join([group for group, freq in sorted_groups])

    def __str__(self):
        return f'{self.user.username} - {self.groups} - {self.tendency}'


