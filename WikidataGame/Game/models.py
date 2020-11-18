from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import make_aware


class Question(models.Model):
    '''
    The Question Model contains all details regarding a question
    '''
    question_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=100, blank=True, null=True)
    question_object = models.CharField(max_length=200, null=True)
    question_property = models.CharField(max_length=200, null=True)
    number_of_views = models.FloatField(default=0)
    age = models.FloatField(default=0)
    is_updated = models.BooleanField(default=False)
    correct_answer = models.CharField(max_length=200, null=True)
    reference = models.URLField(null=True)


class Answer(models.Model):
    '''
    The Answer Model contains answers entered by a user as well as the question
    '''
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=0)
