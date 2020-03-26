from django.db import models
from datetime import datetime


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now())


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasks')
    task_name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now())
    is_done = models.BooleanField(default=False)

