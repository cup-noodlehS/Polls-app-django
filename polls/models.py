import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Set(models.Model):
    set_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    votes_num = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
