from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import make_aware

# Create your models here.


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=100, blank=True, null=True)
    question_hin = models.CharField(max_length=200)
    number_of_views = models.FloatField(default=0)
    age = models.FloatField(default=0)
    is_updated = models.BooleanField(default=False)
    question_eng = models.CharField(max_length=200, null=True)
    correct_answer = models.CharField(max_length=200, null=True)
    reference = models.URLField(null=True)


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=0)
