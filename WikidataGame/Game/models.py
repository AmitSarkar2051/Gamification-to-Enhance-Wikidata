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
    correct_answer = models.CharField(max_length=200)
    reference = models.URLField()
    question_eng = models.CharField(max_length=200)
    correctness_score = models.FloatField(default=0)


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=0)
