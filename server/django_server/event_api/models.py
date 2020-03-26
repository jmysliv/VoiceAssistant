from django.db import models
from datetime import datetime


class Event(models.Model):
    user_id = models.CharField(max_length=200)
    event_name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now())


class Task(models.Model):
    user_id = models.CharField(max_length=200)
    task_name = models.CharField(max_length=100)
    date = models.DateTimeField(blank=True)
    is_done = models.BooleanField(default=False)

